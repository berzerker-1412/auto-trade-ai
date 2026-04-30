#!/usr/bin/env python3
"""
Auto Trade AI - Main Entry Point

Usage:
    python main.py --mode paper --asset crypto
    python main.py --mode live --asset crypto
    python main.py --mode paper --asset gold
    python main.py --mode live --asset both --wallet live
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.trader import Trader
from backend.core.wallet_manager import WalletManager
from backend.core.models import AssetType, WalletType
from backend.crypto.exchange import CryptoExchange
from backend.gold.price_feed import GoldPriceFeed
from backend.ai.signal_generator import AISignalGenerator


def parse_args():
    parser = argparse.ArgumentParser(description="Auto Trade AI")
    parser.add_argument(
        "--mode",
        choices=["paper", "live"],
        default="paper",
        help="Trading mode: paper (simulation) or live (real money)"
    )
    parser.add_argument(
        "--asset",
        choices=["crypto", "gold", "both"],
        default="both",
        help="Asset type to trade"
    )
    parser.add_argument(
        "--symbol",
        default=None,
        help="Specific symbol to trade (e.g., BTC/USDT)"
    )
    parser.add_argument(
        "--balance",
        type=float,
        default=100000,
        help="Initial balance for paper trading"
    )
    parser.add_argument(
        "--wallet",
        choices=["paper", "live"],
        default="paper",
        help="Wallet type: paper (simulated) or live (real exchange)"
    )
    return parser.parse_args()


def run_crypto_trader(args):
    """Run crypto trading"""
    print(f"\n{'='*50}")
    print("CRYPTO TRADER - Auto Trade AI")
    print(f"{'='*50}")
    print(f"Mode: {'PAPER TRADE' if args.mode == 'paper' else 'LIVE TRADING'}")
    print(f"Wallet: {args.wallet.upper()}")
    
    # Initialize WalletManager — แยกกระเป๋าตัง PAPER กับ LIVE
    wm = WalletManager(paper_initial=args.balance)
    wallet_type = WalletType.LIVE if args.wallet == "live" else WalletType.PAPER

    # Initialize exchange — testnet สำหรับ PAPER, real สำหรับ LIVE
    exchange = CryptoExchange(testnet=(args.wallet == "paper"))
    
    # Initialize AI
    ai = AISignalGenerator()
    
    # Initialize trader with wallet type
    trader = Trader(
        wallet_manager=wm,
        wallet_type=wallet_type,
    )
    print(f"Initial Balance: {args.balance} USDT")
    
    # Get supported symbols
    symbols = [args.symbol] if args.symbol else ["BTC/USDT", "ETH/USDT"]
    
    print(f"\nMonitoring: {', '.join(symbols)}")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            for symbol in symbols:
                # Get market data
                ticker = exchange.get_ticker(symbol)
                if not ticker:
                    continue
                
                print(f"\n[{symbol}] Price: {ticker.get('last', 'N/A')}")
                
                # Get historical data for analysis
                ohlcv = exchange.get_ohlcv(symbol, limit=24)
                price_data = [
                    {"price": candle[4], "high": candle[2], "low": candle[3]}
                    for candle in ohlcv[-10:]
                ]
                
                # Analyze and generate signal
                analysis = ai.analyze_market(symbol, price_data)
                signal = ai.generate_signal(
                    symbol=symbol,
                    asset_type=AssetType.CRYPTO,
                    market_data=ticker
                )
                
                if signal:
                    print(f"  Signal: {signal.direction.value.upper()} "
                          f"(confidence: {signal.confidence:.0%})")
                    
                    if signal.direction.value == "buy":
                        trade = trader.execute_signal(signal)
                    else:
                        # Close existing position
                        trader.close_trade(symbol, ticker.get("last"))
            
            asyncio.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        print("\n\nStopping trader...")
        stats = trader.get_stats()
        print(f"\nFinal Balance: {stats['current_balance']} USDT")
        print(f"Total Trades: {stats['total_trades']}")
        print(f"Win Rate: {stats['win_rate']}")


def run_gold_trader(args):
    """Run gold trading"""
    print(f"\n{'='*50}")
    print("GOLD TRADER - Auto Trade AI")
    print(f"{'='*50}")
    print(f"Mode: {'PAPER TRADE' if args.mode == 'paper' else 'LIVE TRADING'}")
    print(f"Wallet: {args.wallet.upper()}")
    
    # Initialize gold price feed — ใช้ real API (alpha_vantage)
    gold = GoldPriceFeed()
    
    # Initialize WalletManager
    wm = WalletManager(paper_initial=args.balance)
    wallet_type = WalletType.LIVE if args.wallet == "live" else WalletType.PAPER

    # Initialize AI
    ai = AISignalGenerator()
    
    # Initialize trader
    trader = Trader(
        wallet_manager=wm,
        wallet_type=wallet_type,
    )
    print(f"Initial Balance: ${args.balance}")
    
    symbol = "XAUUSD"
    print(f"\nMonitoring: GOLD ({symbol})")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            price_data = gold.get_price(symbol)
            if price_data:
                print(f"\n[{symbol}] Price: ${price_data.get('price', 'N/A')}")
                
                # Generate signal
                signal = ai.generate_signal(
                    symbol=symbol,
                    asset_type=AssetType.GOLD,
                    market_data=price_data
                )
                
                if signal:
                    print(f"  Signal: {signal.direction.value.upper()} "
                          f"(confidence: {signal.confidence:.0%})")
                    
                    if signal.direction.value == "buy":
                        trade = trader.execute_signal(signal)
            
            asyncio.sleep(15)  # Check every 15 seconds
            
    except KeyboardInterrupt:
        print("\n\nStopping trader...")
        stats = trader.get_stats()
        print(f"\nFinal Balance: ${stats['current_balance']}")
        print(f"Total Trades: {stats['total_trades']}")


def main():
    args = parse_args()
    
    if args.asset in ["crypto", "both"]:
        run_crypto_trader(args)
    
    if args.asset in ["gold", "both"]:
        run_gold_trader(args)


if __name__ == "__main__":
    main()
