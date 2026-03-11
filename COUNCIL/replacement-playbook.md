# Council Replacement Playbook

## Trigger criteria
Mark a member for replacement if BOTH are true:
- zero_vote_streak >= 10 rounds
- selection_rate < 5% over last 30 rounds

## Replacement flow
1. Move member to `retiredMembers` in `COUNCIL/roster.yaml`
2. Add replacement as `status: probation`
3. Run 10 probation rounds
4. Promote to active if quality is acceptable and no safety veto issues
