"""Wallet Manager — จัดการกระเป๋าตังแยกระหว่าง PAPER กับ LIVE"""

from typing import Dict, Optional
from .models import Wallet, WalletType


class WalletManager:
    """
    จัดการกระเป๋าตัง 2 ใบแยกจากกัน:
    - PAPER: กระเป๋าจำลอง ไม่ใช้เงินจริง
    - LIVE:  กระเป๋าจริง เชื่อมกับ exchange wallet

    ทั้งสองใช้งานพร้อมกันได้ — ทดสอบระบบด้วย PAPER ก่อน แล้วค่อยเทรดจริงด้วย LIVE
    """

    def __init__(
        self,
        paper_initial: float = 100000.0,
        paper_currency: str = "USDT",
        live_currency: str = "USDT",
    ):
        self.paper_wallet = Wallet(
            wallet_type=WalletType.PAPER,
            balance=paper_initial,
            currency=paper_currency,
        )
        self.live_wallet = Wallet(
            wallet_type=WalletType.LIVE,
            balance=0.0,  # ยอดจริงได้จาก exchange API
            currency=live_currency,
        )

    def get_wallet(self, wallet_type: WalletType) -> Wallet:
        """ดึงกระเป๋าตังตามประเภท"""
        if wallet_type == WalletType.PAPER:
            return self.paper_wallet
        return self.live_wallet

    def update_balance(self, wallet_type: WalletType, new_balance: float):
        """อัปเดตยอดกระเป๋าตัง (เรียกจาก exchange API สำหรับ LIVE)"""
        wallet = self.get_wallet(wallet_type)
        wallet.balance = new_balance

    def reset_paper_wallet(self, new_balance: Optional[float] = None):
        """รีเซ็ตกระเป๋าตังจำลอง — เหมาะตอนเริ่มรอบทดสอบใหม่"""
        if new_balance is not None:
            self.paper_wallet.balance = new_balance
            self.paper_wallet.initial_balance = new_balance
        else:
            self.paper_wallet.balance = self.paper_wallet.initial_balance

    def get_summary(self) -> Dict:
        """สรุปยอดทั้งสองกระเป๋า"""
        return {
            "paper": self.paper_wallet.to_dict(),
            "live": self.live_wallet.to_dict(),
        }
