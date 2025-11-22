.PHONY: python-validate python-export dot-check js web ci ci-docker

python-validate:
	python tools/validate_shapes.py

python-export:
	python tools/export_instances_dot.py
	python tools/export_web_json.py

dot-check:
	@set -e; \
	dot -Tsvg goblin-map.dot -o docs/goblin-map.svg.new; \
	dot -Tpng goblin-map.dot -o docs/goblin-map.png.new; \
	cmp -s docs/goblin-map.svg docs/goblin-map.svg.new; \
	cmp -s docs/goblin-map.png docs/goblin-map.png.new

js:
	cd js/goblin-ontology && (npm ci || npm i) && npm run typecheck && npm run build && npm test

web:
	cd web && (npm ci || npm i) && npm run build

ci: python-validate python-export dot-check js web

ci-docker:
	docker compose run --rm python-validate
	docker compose run --rm python-export
	docker compose run --rm dot-check
	docker compose run --rm js-package
	docker compose run --rm web-build

.PHONY: hooks hooks-push
hooks:
	pre-commit run --all-files --show-diff-on-failure

hooks-push:
	pre-commit run --all-files --hook-stage push --show-diff-on-failure


