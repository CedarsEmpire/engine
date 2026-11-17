# api/withdraw.py - ENGINE FIVE - Crypto Withdraw Only
import os
from supabase import create_client

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def handler(request):
    # Only allow POST
    if request.method != "POST":
        return {"error": "POST only"}, 405

    data = request.json
    user_id = data.get("user_id")
    wallet = data.get("wallet_address")
    amount = float(data.get("amount", 0))
    currency = data.get("currency", "USDT")
    network = data.get("network", "TRC20")

    if not wallet or amount <= 0:
        return {"error": "Wallet address and amount required"}, 400

    # 1. Get user balance
    user = supabase.table("users").select("balance_gbp").eq("id", user_id).execute()
    if not user.data:
        return {"error": "User not found"}, 404

    balance = float(user.data[0]["balance_gbp"])

    # 2. Check balance - your page shows £1.00
    if amount > balance:
        return {"error": "Insufficient balance"}, 400

    if amount < 1.0:
        return {"error": "Minimum withdraw is £1.00"}, 400

    # 3. Create withdraw request - PENDING for you to approve/pay
    withdraw = supabase.table("withdrawals").insert({
        "user_id": user_id,
        "amount_gbp": amount,
        "currency": currency,
        "network": network,
        "wallet_address": wallet,
        "status": "pending"
    }).execute()

    # 4. Deduct balance
    supabase.table("users").update({
        "balance_gbp": balance - amount
    }).eq("id", user_id).execute()

    return {
        "success": True,
        "message": f"Withdraw {amount} GBP in {currency} ({network}) requested",
        "wallet": wallet,
        "status": "pending"
    }, 200
