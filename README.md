## Learn Supaku In-Depth 😂
- Subak 🍉
## TODOs
- [x] Fake gen
- [x] docker compose
- [x] do complex ops
- [ ] volume QoL(local-jupyter-spark)
- [ ] optimize
    - [ ] 100 fold data
    - [ ] partitioning
    - [ ] graph shows that broadcast is automatic. see if explicit broadcast has any other effect?
    - [ ] if broadcast is not an option(both df are huge) try sortMergeJoin and bucketBy
    - [ ] use of joined.cache()
    - [ ] repartition by other column for downstream groupbys
    - [ ] column pruning (predicate pushdown at work): select only the necessary columns
    - [ ] handling already partitioned parquets
- [ ] try df.explain(True)
- [ ] helm chart packaging
- [ ] cluster deployment

This picture demonstrates that broadcast is autocast 😁
![alt text](image-2.png)

## Test results
### Notes
- data should exist on worker node as well -> add volume
### test_submission.py result
- Agg1 result
![Aggregation one](image.png)
- Top spenders result
![alt text](image-1.png)