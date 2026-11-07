#!/bin/bash
# usage: tools/q.sh topic... -> compact chapter SQL
python3 -I tools/chapter_sql.py "$@" | python3 -c "
import sys
s=sys.stdin.read()
s=s.replace('c.key_takeaways[1:5] takeaways','left(c.key_takeaways::text,380) takeaways')
s=s.replace('c.key_takeaways takeaways','left(c.key_takeaways::text,380) takeaways')
s=s.replace('left(c.analogy_body, 700)','left(c.analogy_body, 160)')
s=s.replace(\"'right',x->>'right'\",\"'right',left(x->>'right',70)\").replace('limit 2) q','limit 3) q')
print(s)"
