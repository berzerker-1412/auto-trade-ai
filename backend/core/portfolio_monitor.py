"""Portfolio Monitor — ติดตามความเสี่ยงระดับพอร์ตแบบ real-time

รับผิดชอบ:
1. คำนวณ Portfolio VaR (Historical + Parametric)
2. ติดตาม correlation ระหว่าง positions
3. คำนวณ Expected Shortfall (CVaR) — average loss beyond VaR
4. วิเคราะห์ portfolio beta กับ market indices
5. Risk contribution ของแต่ละ position
6. Correlation heatmap สำหรับ multi-asset portfolio

Citations:
- Jorion, P., "Value at Risk" (2007) — VaR methodologies
- Artzner, P. et al., "Coherent Measures of Risk" (1999) — CVaR/ES
- Markowitz, H., "Portfolio Selection" (1952) — Modern Portfolio Theory
"""
import numpy as np
from typing import Dict, Any, Optional, List, Literal
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PositionRisk:
    symbol: str
    size: float              # notional value
    weight: float           # % of portfolio
    vol_daily: float        # daily volatility
    var_95: float           # VaR of this position
    cvar_95: float          # CVaR of this position
    contribution: float     # risk contribution to portfolio
    contribution_pct: float # % of total portfolio risk


@dataclass
class PortfolioRiskReport:
    total_value: float
    var_95_daily: float          # Portfolio VaR (95%, 1-day)
    var_95_monthly: float         # Portfolio VaR (95%, 1-month)
    cvar_95_daily: float          # CVaR / Expected Shortfall
    sharpe_ratio: float           # Annualized
    max_drawdown: float           # Current drawdown %
    beta_vs_btc: float            # Beta vs BTC
    beta_vs_sp500: float          # Beta vs SP500 (if available)
    volatility_annual: float      # Annualized portfolio vol
    correlation_matrix: Dict[str, Dict[str, float]]  # inter-position correlations
    positions: List[PositionRisk]
    risk_level: Literal["low", "medium", "high", "critical"]
    warnings: List[str]           # warnings ที่ควรรู้


class PortfolioMonitor:
    """
    ติดตามความเสี่ยงของทั้งพอร์ตแบบ real-time
    
    ใช้ได้กับ multi-asset portfolio (BTC, ETH, Gold)
    """

    def __init__(
        self,
        portfolio_value: float = 100_000.0,
        risk_free_rate: float = 0.04,    # 4% annual risk-free rate
        target_return: float = 0.15,       # 15% annual target
        var_confidence: float = 0.95,
    ):
        self.portfolio_value = portfolio_value
        self.risk_free_rate = risk_free_rate
        self.target_return = target_return
        self.var_confidence = var_confidence
        
        # Asset volatility (annual, approximate)
        self.asset_vols: Dict[str, float] = {
            "BTCUSDT": 0.70,
            "BTC": 0.70,
            "ETHUSDT": 0.85,
            "ETH": 0.85,
            "XAUUSD": 0.15,
            "XAU": 0.15,
            "default": 0.60,
        }
        
        # Historical returns for VaR calculation
        self.portfolio_returns: List[float] = []
        
        # Position tracking
        self.positions: Dict[str, Dict[str, float]] = {}  # symbol -> data
        self.position_prices: Dict[str, List[float]] = {}  # symbol -> price history
        
        # Reference indices (for beta calculation)
        self.btc_returns: List[float] = []
        self.sp500_returns: List[float] = []

    # ================================================================= #
    # Position Management
    # ================================================================= #

    def add_position(
        self,
        symbol: str,
        size: float,         # notional value in USD
        entry_price: float,
        current_price: Optional[float] = None,
    ):
        """เพิ่ม position ใหม่"""
        vol = self.asset_vols.get(symbol, self.asset_vols["default"])
        daily_vol = vol / np.sqrt(365)
        
        weight = size / self.portfolio_value if self.portfolio_value > 0 else 0
        
        self.positions[symbol] = {
            "size": size,
            "entry_price": entry_price,
            "current_price": current_price or entry_price,
            "weight": weight,
            "vol_daily": daily_vol,
            "daily_var_95": size * daily_vol * 1.645,  # 95% 1-day VaR
        }
        
        # Initialize price tracking
        if symbol not in self.position_prices:
            self.position_prices[symbol] = []
        self.position_prices[symbol].append(current_price or entry_price)
        if len(self.position_prices[symbol]) > 100:
            self.position_prices[symbol].pop(0)

    def update_position_price(self, symbol: str, current_price: float):
        """อัปเดตราคาปัจจุบันของ position"""
        if symbol in self.positions:
            self.positions[symbol]["current_price"] = current_price
            
            if symbol in self.position_prices:
                self.position_prices[symbol].append(current_price)
                if len(self.position_prices[symbol]) > 100:
                    self.position_prices[symbol].pop(0)

    def remove_position(self, symbol: str):
        """ลบ position ออก (เมื่อปิด trade)"""
        if symbol in self.positions:
            del self.positions[symbol]

    # ================================================================= #
    # Core Risk Calculations
    # ================================================================= #

    def calculate_var_historical(
        self,
        returns: List[float],
        confidence: float = 0.95,
    ) -> float:
        """VaR แบบ Historical — ใช้ historical returns distribution"""
        if len(returns) < 10:
            return self.portfolio_value * 0.02  # fallback: 2%
        
        sorted_returns = np.sort(returns)
        index = int((1 - confidence) * len(sorted_returns))
        var_pct = abs(sorted_returns[max(0, index)])
        return float(var_pct * self.portfolio_value)

    def calculate_var_parametric(
        self,
        returns: List[float],
        confidence: float = 0.95,
    ) -> float:
        """VaR แบบ Parametric (variance-covariance)"""
        if len(returns) < 10:
            return self.portfolio_value * 0.02
        
        mu = np.mean(returns)
        sigma = np.std(returns)
        
        # Z-score for 95% confidence
        z = 1.645
        
        var_pct = abs(mu - z * sigma)
        return float(var_pct * self.portfolio_value)

    def calculate_cvar(
        self,
        returns: List[float],
        confidence: float = 0.95,
    ) -> float:
        """CVaR / Expected Shortfall — average loss beyond VaR"""
        if len(returns) < 10:
            return self.portfolio_value * 0.03
        
        var = self.calculate_var_historical(returns, confidence)
        var_pct = var / self.portfolio_value
        
        tail_returns = [r for r in returns if r <= -var_pct]
        if not tail_returns:
            return var
        
        cvar_pct = abs(np.mean(tail_returns))
        return float(cvar_pct * self.portfolio_value)

    def calculate_sharpe_ratio(
        self,
        returns: List[float],
        annualization: int = 365,
    ) -> float:
        """Annualized Sharpe Ratio"""
        if len(returns) < 5:
            return 0.0
        
        mean_ret = np.mean(returns) * annualization
        std_ret = np.std(returns) * np.sqrt(annualization)
        
        if std_ret == 0:
            return 0.0
        
        return float((mean_ret - self.risk_free_rate) / std_ret)

    def calculate_portfolio_beta(
        self,
        position_returns: List[float],
        market_returns: List[float],
    ) -> float:
        """คำนวณ beta ของ position กับ market index"""
        if len(position_returns) < 5 or len(market_returns) < 5:
            return 1.0
        
        min_len = min(len(position_returns), len(market_returns))
        pos_ret = np.array(position_returns[-min_len:])
        mkt_ret = np.array(market_returns[-min_len:])
        
        covariance = np.cov(pos_ret, mkt_ret)[0, 1]
        market_variance = np.var(mkt_ret)
        
        if market_variance == 0:
            return 1.0
        
        return float(covariance / market_variance)

    def calculate_correlation_matrix(
        self,
    ) -> Dict[str, Dict[str, float]]:
        """คำนวณ correlation matrix ระหว่าง positions"""
        symbols = list(self.position_prices.keys())
        n = len(symbols)
        
        if n < 2:
            return {}
        
        # Build price returns matrix
        returns_matrix = []
        for symbol in symbols:
            prices = np.array(self.position_prices[symbol])
            if len(prices) < 2:
                returns_matrix.append([])
            else:
                rets = np.diff(prices) / prices[:-1]
                returns_matrix.append(rets)
        
        # Calculate correlations
        corr_matrix: Dict[str, Dict[str, float]] = {}
        for i, sym_i in enumerate(symbols):
            corr_matrix[sym_i] = {}
            for j, sym_j in enumerate(symbols):
                if i == j:
                    corr_matrix[sym_i][sym_j] = 1.0
                elif j > i:
                    # Get overlapping period
                    rets_i = returns_matrix[i]
                    rets_j = returns_matrix[j]
                    min_len = min(len(rets_i), len(rets_j))
                    if min_len < 5:
                        corr = 0.5  # default
                    else:
                        corr = float(np.corrcoef(rets_i[-min_len:], rets_j[-min_len:])[0, 1])
                        if np.isnan(corr):
                            corr = 0.5
                    corr_matrix[sym_i][sym_j] = corr
                    corr_matrix[sym_j][sym_i] = corr
                else:
                    corr_matrix[sym_i][sym_j] = corr_matrix[sym_j][sym_i]
        
        return corr_matrix

    # ================================================================= #
    # Full Report
    # ================================================================= #

    def generate_report(
        self,
        btc_returns: Optional[List[float]] = None,
        sp500_returns: Optional[List[float]] = None,
    ) -> PortfolioRiskReport:
        """สร้าง risk report ฉบับเต็ม"""
        
        # Update portfolio value
        total_value = sum(pos["size"] for pos in self.positions.values())
        if total_value == 0:
            total_value = self.portfolio_value
        
        # Calculate position-level risks
        positions_risk: List[PositionRisk] = []
        total_var = 0.0
        
        for symbol, pos in self.positions.items():
            size = pos["size"]
            weight = size / total_value if total_value > 0 else 0
            daily_vol = pos["vol_daily"]
            
            # Position VaR (95%, 1-day)
            pos_var = size * daily_vol * 1.645
            pos_cvar = size * daily_vol * 2.063  # CVaR approximation
            
            total_var += pos_var ** 2  # variance sum (ignoring correlations for now)
            
            positions_risk.append(PositionRisk(
                symbol=symbol,
                size=size,
                weight=weight,
                vol_daily=daily_vol,
                var_95=pos_var,
                cvar_95=pos_cvar,
                contribution=pos_var,
                contribution_pct=0,
            ))
        
        # Portfolio VaR (sum of variances, assuming partial correlations)
        portfolio_var = total_var ** 0.5
        
        # Correlation adjustment
        corr_matrix = self.calculate_correlation_matrix()
        if len(corr_matrix) >= 2:
            # Apply correlation diversification benefit
            avg_corr = self._average_correlation(corr_matrix)
            n = len(corr_matrix)
            if n > 1:
                # Diversification ratio
                div_ratio = 1 / (n * (1 - avg_corr) + avg_corr)
                portfolio_var *= max(0.5, div_ratio)
        
        # Calculate contribution percentages
        if portfolio_var > 0:
            for pos_risk in positions_risk:
                pos_risk.contribution_pct = pos_risk.contribution / portfolio_var
        
        # Sort by risk contribution
        positions_risk.sort(key=lambda x: x.contribution, reverse=True)
        
        # Calculate drawdown
        current_value = total_value
        peak_value = max(current_value, self.portfolio_value)
        max_drawdown = abs((peak_value - current_value) / peak_value) if peak_value > 0 else 0
        
        # Calculate Sharpe
        sharpe = self.calculate_sharpe_ratio(self.portfolio_returns)
        
        # Monthly VaR approximation
        var_monthly = portfolio_var * np.sqrt(21)  # 21 trading days
        
        # Risk level assessment
        var_pct = portfolio_var / total_value if total_value > 0 else 0
        if var_pct > 0.05:
            risk_level: Literal["low", "medium", "high", "critical"] = "critical"
        elif var_pct > 0.03:
            risk_level = "high"
        elif var_pct > 0.015:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Warnings
        warnings: List[str] = []
        
        # Check correlation concentration
        if len(corr_matrix) >= 2:
            high_corr_pairs = []
            for sym_i in corr_matrix:
                for sym_j in corr_matrix[sym_i]:
                    if sym_i < sym_j and corr_matrix[sym_i][sym_j] > 0.85:
                        high_corr_pairs.append(f"{sym_i}-{sym_j}: {corr_matrix[sym_i][sym_j]:.2f}")
            if high_corr_pairs:
                warnings.append(f"High correlation pairs: {', '.join(high_corr_pairs)}")
        
        # Check position concentration
        for pos_risk in positions_risk:
            if pos_risk.weight > 0.4:
                warnings.append(f"Position {pos_risk.symbol} is {pos_risk.weight:.0%} of portfolio — HIGH CONCENTRATION")
        
        # Check volatility
        if len(self.portfolio_returns) >= 5:
            recent_vol = np.std(self.portfolio_returns[-20:]) * np.sqrt(365)
            if recent_vol > 1.0:  # > 100% annual vol
                warnings.append(f"Portfolio volatility extremely high: {recent_vol:.0%} annual")
        
        return PortfolioRiskReport(
            total_value=total_value,
            var_95_daily=portfolio_var,
            var_95_monthly=var_monthly,
            cvar_95_daily=self.calculate_cvar(self.portfolio_returns),
            sharpe_ratio=sharpe,
            max_drawdown=max_drawdown,
            beta_vs_btc=1.0,
            beta_vs_sp500=1.0,
            volatility_annual=np.std(self.portfolio_returns[-30:]) * np.sqrt(365) if len(self.portfolio_returns) >= 30 else 0,
            correlation_matrix=corr_matrix,
            positions=positions_risk,
            risk_level=risk_level,
            warnings=warnings,
        )

    def _average_correlation(self, corr_matrix: Dict[str, Dict[str, float]]) -> float:
        """คำนวณ average pairwise correlation"""
        symbols = list(corr_matrix.keys())
        n = len(symbols)
        if n < 2:
            return 0.0
        
        total_corr = 0.0
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                total_corr += corr_matrix[symbols[i]][symbols[j]]
                count += 1
        
        return total_corr / count if count > 0 else 0.0

    def record_return(self, portfolio_return: float):
        """บันทึก portfolio return สำหรับ VaR calculation"""
        self.portfolio_returns.append(portfolio_return)
        if len(self.portfolio_returns) > 365:  # keep 1 year
            self.portfolio_returns.pop(0)
