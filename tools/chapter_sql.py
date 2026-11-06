"""python3 -I tools/chapter_sql.py topic1 topic2 ... -> SQL that returns compact chapter material for each topic."""
import json, sys
m = json.load(open("data/topic-map.json"))
rows = []
for t in sys.argv[1:]:
    sl = m[t]["slugs"]
    pri = [s for s in sl if not s.startswith(("lab-", "troubleshoot-", "exam-trap")) and not s.endswith("-netplus")] or sl
    rows.append(f"('{t}','{pri[0]}')")
print("""select v.t, c.analogy_title, left(c.analogy_body, 700) analogy, c.key_takeaways[1:5] takeaways,
 (select jsonb_agg(jsonb_build_object('wrong',x->>'wrong','right',x->>'right')) from (select x from jsonb_array_elements(c.misconceptions) x limit 3) q) mis
from (values """ + ",".join(rows) + """) v(t,s)
join lateral (select * from exam_topic_chapters where topic_slug=v.s order by (exam_slug='ccna') desc, (exam_slug='network-plus') desc limit 1) c on true""")
