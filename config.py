USERNAME="github username"
TOKEN="github access token"
USER="organization"
PROJECT="repository"
MIN_ID=None
MAX_ID=None

BASE_URL="https://api.github.com/"
CACHE_DIR="cache/"

LABELS_TO_FIELDS = {
  "Component": {
    "PHABRICATOR_FIELD": "com.organization.component",
    "GITHUB_LABEL_PATTERN": "^Component:\s+(.*)"
  },
  "Product": {
    "PHABRICATOR_FIELD": "com.organization.product",
    "GITHUB_LABEL_PATTERN": "^Product:\s+(.*)"
  }
}
