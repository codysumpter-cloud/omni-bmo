# Council Strict Mode

Status: ENABLED

## Behavior
For user-facing answers by default:
1. Run council voting protocol.
2. Log participants and winner.
3. Return only winning final answer to user.

## Allowed exceptions
- trivial acknowledgements
- urgent safety warning messages
- low-risk progress pings

If exception used, log reason when practical.
