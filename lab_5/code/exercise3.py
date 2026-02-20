"""
Exercise 3: Self-Rechecking PR Loop
"""
from exercise1 import review_pr 
from exercise2 import generate_fix

def review_until_approved(code: str, max_rounds=3):
    current_code = code

    for round in range(1, max_rounds + 1):
        print(f"\n--- Review Round {round} ---\n")

        review = review_pr(current_code)
        print(review.model_dump_json(indent=2))

        if review.approve:
            print("\nPR APPROVED")
            return current_code

        patch = generate_fix(current_code, review)
        print("\nApplying Patch\n")
        print(patch.explanation)

        current_code = patch.fixed_code

    print("\nPR NOT APPROVED AFTER MAX ROUNDS")
    return current_code


if __name__ == "__main__":
    buggy_code_example_1 = """
    def divide_numbers(a, b):
        return a / b

    def average(nums):
        total = 0
        for n in nums:
            total += n
        return total / len(nums)
    """

    
    final_code = review_until_approved(buggy_code_example_1)
    print("\nFINAL CODE:\n")
    print(final_code)