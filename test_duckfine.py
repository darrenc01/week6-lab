import unittest
from duckfine import DuckFine


class TestDuckFineInit(unittest.TestCase):
    """Tests for __init__ behaviour."""

    def test_member_id_stored(self):
        duck = DuckFine("A42")
        self.assertEqual(duck.member_id, "A42")

    def test_total_owed_starts_at_zero(self):
        duck = DuckFine("A42")
        self.assertEqual(duck.total_owed, 0.0)


class TestDuckFineCharge(unittest.TestCase):
    """Tests for the charge() method."""

    def setUp(self):
        self.duck = DuckFine("M01")

    # ------------------------------------------------------------------
    # Grace period
    # ------------------------------------------------------------------

    def test_zero_days_late_has_no_fee(self):
        fee = self.duck.charge(0)
        self.assertEqual(fee, 0.0)

    def test_within_grace_period_has_no_fee(self):
        """1 or 2 days late are fully within the grace period."""
        fee = self.duck.charge(2)
        self.assertEqual(fee, 0.0)

    # ------------------------------------------------------------------
    # Normal (non-deluxe) charges
    # ------------------------------------------------------------------

    def test_one_day_beyond_grace_charges_daily_fee(self):
        """3 days late -> 1 chargeable day -> $0.50."""
        fee = self.duck.charge(3)
        self.assertAlmostEqual(fee, 0.50)

    def test_fee_scales_with_chargeable_days(self):
        """5 days late -> 3 chargeable days -> $1.50."""
        fee = self.duck.charge(5)
        self.assertAlmostEqual(fee, 1.50)

    def test_fee_capped_at_max_fee(self):
        """Many days late should never exceed MAX_FEE ($5.00)."""
        fee = self.duck.charge(100)
        self.assertEqual(fee, DuckFine.MAX_FEE)

    def test_fee_exactly_at_cap_boundary(self):
        """12 days late -> 10 chargeable days -> $5.00, exactly the cap."""
        fee = self.duck.charge(12)
        self.assertAlmostEqual(fee, 5.00)

    # ------------------------------------------------------------------
    # Deluxe (double-rate) charges
    # ------------------------------------------------------------------

    def test_deluxe_doubles_the_fee(self):
        """3 days late, deluxe -> $0.50 x 2 = $1.00."""
        fee = self.duck.charge(3, deluxe=True)
        self.assertAlmostEqual(fee, 1.00)

    def test_deluxe_still_capped_at_max_fee(self):
        """Doubling cannot push the fee above MAX_FEE."""
        fee = self.duck.charge(100, deluxe=True)
        self.assertEqual(fee, DuckFine.MAX_FEE)

    def test_deluxe_within_grace_period_has_no_fee(self):
        """Even deluxe ducks owe nothing inside the grace period."""
        fee = self.duck.charge(1, deluxe=True)
        self.assertEqual(fee, 0.0)

    # ------------------------------------------------------------------
    # Accumulation of total_owed
    # ------------------------------------------------------------------

    def test_total_owed_accumulates_across_charges(self):
        """Multiple charges sum into total_owed."""
        self.duck.charge(3)   # $0.50
        self.duck.charge(5)   # $1.50
        self.assertAlmostEqual(self.duck.total_owed, 2.00)

    def test_zero_fee_charge_does_not_change_total_owed(self):
        self.duck.charge(1)
        self.assertEqual(self.duck.total_owed, 0.0)

    def test_total_owed_independent_between_instances(self):
        other = DuckFine("M99")
        self.duck.charge(3)   # $0.50 on self.duck
        self.assertEqual(other.total_owed, 0.0)

    # ------------------------------------------------------------------
    # Return value
    # ------------------------------------------------------------------

    def test_charge_returns_fee_not_total_owed(self):
        """charge() must return only the current fee, not the running total."""
        self.duck.charge(3)   # accumulate some debt first
        fee = self.duck.charge(4)  # 2 chargeable days -> $1.00
        self.assertAlmostEqual(fee, 1.00)

    # ------------------------------------------------------------------
    # Input validation
    # ------------------------------------------------------------------

    def test_negative_days_late_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.duck.charge(-1)

    def test_negative_days_late_error_message(self):
        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            self.duck.charge(-5)


if __name__ == "__main__":
    unittest.main()
