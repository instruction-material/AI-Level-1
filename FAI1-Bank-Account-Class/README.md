# Bank Account Class

Run `python3 main.py`. The worked balance sequence is 0, 1000, 1100, then 100. Withdrawing 150 is rejected and keeps the balance at 100.

Deposits and withdrawals accept finite nonnegative numbers, including zero. A negative or nonfinite amount raises `ValueError` before changing the balance. The rate is supplied as a decimal: `0.10` means ten percent. This small class practices instance state and methods; currency rounding and a real ledger are outside the example.
