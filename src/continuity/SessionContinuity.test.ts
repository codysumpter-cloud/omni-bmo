import { SessionManager, SessionState } from "./SessionManager";

describe("SessionContinuity", () => {
  it("should initialize session manager", () => {
    const sm = new SessionManager();
    expect(sm).toBeDefined();
  });
});
