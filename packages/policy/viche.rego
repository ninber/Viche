package viche.authz

default allow := false

allow if {
  input.action == "health.read"
}

allow if {
  input.subject.role == "operator"
  input.action == "proposal.moderate"
}

allow if {
  input.subject.role == "member"
  input.action == "proposal.submit"
}

allow if {
  input.subject.role == "operator"
  input.action == "federation.artifact.triage"
}

allow if {
  input.subject.role == "operator"
  input.action == "federation.relationship.manage"
}
