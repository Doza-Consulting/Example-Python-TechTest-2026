# One on-demand (pay-per-request) table per entity, keyed on `id`.
# On-demand billing means these cost ~nothing when idle.
resource "aws_dynamodb_table" "rooms" {
  name         = "${local.name}-rooms"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "game_masters" {
  name         = "${local.name}-game-masters"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "bookings" {
  name         = "${local.name}-bookings"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
