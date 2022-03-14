import os
import subprocess


def sync_subscriptions():
    subprocess.run(
        "python manage.py djstripe_sync_models Subscription",
        shell=True,
        env=os.environ.copy(),
        capture_output=True,
    )
