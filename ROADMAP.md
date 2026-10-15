# 90 daily tasks

One numbered task per day. The runner selects the first ID absent from `progress.json`.

## Month 1 — foundation

01. Document architecture in `docs/architecture.md`; check the file exists.
02. Add API version to health response; test exact field.
03. Add database readiness endpoint; test failure path.
04. Add database session factory; test configuration.
05. Add project model; test metadata.
06. Add task model; test metadata.
07. Add versioned schema SQL in `docs/schema-v1.sql`; check PostgreSQL syntax.
08. Add project creation schema; test validation.
09. Add project creation endpoint; test persistence.
10. Add project list endpoint; test ordering.
11. Add project detail endpoint; test missing ID.
12. Add project update endpoint; test validation.
13. Add project deletion endpoint; test missing ID.
14. Add task creation schema; test validation.
15. Add task creation endpoint; test project ownership.
16. Add task list endpoint; test filtering.
17. Add task status update; test transitions.
18. Add API pagination; test boundaries.
19. Add structured errors; test 404.
20. Add request ID middleware; test propagation.
21. Add password hashing; test verification.
22. Add user model; test unique email.
23. Add registration endpoint; test duplicate email.
24. Add login endpoint; test invalid password.
25. Add bearer authentication; test rejection.
26. Add project ownership checks; test cross-user access.
27. Add dashboard project list; check loading state.
28. Add project creation form; check validation.
29. Add planner response schema; test empty goal.
30. Persist planner steps; test round trip.

## Month 2 — agent workflows

31. Add agent run model; test state fields.
32. Add run creation endpoint; test ownership.
33. Add LangGraph planning state; test transition.
34. Add task decomposition node; test schema.
35. Add planner checkpoint storage; test resume.
36. Add run status endpoint; test missing run.
37. Add run timeline UI; check empty state.
38. Add repository connection model; test uniqueness.
39. Add GitHub webhook signature verifier; test bad signature.
40. Add webhook deduplication; test repeated delivery.
41. Add repository metadata client; test mocked response.
42. Add repository permission validation; test denial.
43. Add coding job schema; test path constraints.
44. Add coding job state machine; test transitions.
45. Add patch validator; test path traversal.
46. Add changed-file limit; test oversized proposal.
47. Add coding job timeout; test expiration.
48. Add targeted test selector; test mapping.
49. Add test result parser; test pass and fail.
50. Add one-retry repair decision; test attempt cap.
51. Add review findings schema; test severity.
52. Add secret-pattern review rule; test sample.
53. Add workflow-change review rule; test sample.
54. Add PR summary generator; test evidence.
55. Add evaluation case model; test uniqueness.
56. Add evaluation dataset import; test invalid row.
57. Add deterministic planner evaluation; test score.
58. Add evaluation result storage; test linkage.
59. Add evaluation trend endpoint; test ordering.
60. Add evaluation dashboard; check empty state.

## Month 3 — production

61. Add structured logging; test request ID.
62. Add metrics endpoint; test format.
63. Add latency histogram; test observation.
64. Add agent error counter; test increment.
65. Add PostgreSQL readiness check; test outage.
66. Add transient API retry policy; test cap.
67. Add run idempotency key; test repeat.
68. Add tenant model; test slug.
69. Add tenant membership model; test role.
70. Add tenant context dependency; test missing tenant.
71. Scope projects by tenant; test isolation.
72. Scope tasks by tenant; test isolation.
73. Add tenant invitation endpoint; test expiry.
74. Add tenant run quota; test rejection.
75. Add audit event model; test fields.
76. Log project mutations; test actor.
77. Add secret redaction to logs; test sample.
78. Add dependency audit policy in `docs/dependency-audit.md`; check instructions.
79. Add container healthcheck verification guide; check commands.
80. Add production API deployment checklist; check commands.
81. Add production web deployment checklist; check commands.
82. Add deployment environment example; check variables.
83. Add database backup guide; check restore command.
84. Add incident response guide; check escalation.
85. Add service-level indicators; check definitions.
86. Add API smoke test in `backend/tests`; test local stack.
87. Add accessible dashboard labels; check UI.
88. Add architecture diagram; check against code.
89. Add portfolio case study; check measured claims.
90. Add release checklist and evaluation report; check links.
