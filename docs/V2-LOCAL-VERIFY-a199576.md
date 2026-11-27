# 作者本地复现记录：`release/v2.0` @ `a199576`（作者本地报告）

- **证据性质**：**作者本地报告（非独立第三方验证）**。独立验证记录仍为 **「待验证」**。
- **验证对象**：`PuzzleFF/zfc-patchkit` 提交 `a1995765343359c69b6bf327068f660343e51851`
- **规格文件**：`patches/zfc-v2.json`（SHA-256 `9c1d5e34d55e89baaf5ac437c4959e750da0d4007db66a33d73517d25c8bf172`）
- **日期**：2026-11-27
- **执行命令**：`python tools/verify_release.py --firmware <local official Z_fc_0181.bin>`（输出中的本机绝对路径已脱敏）

## 输出摘要

```text
firmware  Z_fc_0181.bin
  size    35,578,974 (expected 35,578,974) OK
  sha256  e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6
          OK

label                 size  sha256            result
--------------------------------------------------------------
stock           35,021,690  cd47efc126ce5e4c...  MATCH
slowmo25        35,021,690  4a6feaa42c43c7c7...  MATCH
bitrate-a       35,021,690  34c26114878ec886...  MATCH
bitrate-b       35,021,690  3a3a6823a1baf0df...  MATCH
zebra-photo     35,021,690  79c80d6176088fa3...  MATCH
zfc-v1          35,021,690  2c9cc3a91d49f8c1...  MATCH
zfc-v2          35,060,342  b5c6e75ee6cbb09a...  MATCH
--------------------------------------------------------------
all artifacts reproduced and matched -- RESULT PASS
```

## 边界说明
- 本记录仅证明作者本机环境在提交 `a199576` 上由官方 `Z_fc_0181.bin` 复现出的 7 个制品与 `tools/pins.json` 声明的 SHA-256 一致；不构成独立复现验证、实机行为证明或回退保证。
