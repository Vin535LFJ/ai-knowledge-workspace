"""数据源适配器包（增量新增）。

当前仅提供离线 stub，绝不发起任何真实网络请求。未来接入真实数据源时：
- 令牌等敏感信息只能通过环境变量读取，不得硬编码在源码/配置/日志中；
- 默认注入客户端仍是 fixtures/client.py，本包不替换默认行为。

接口见 base.py::SourceClient（与 collector.ApiClient 协议对齐）。
"""
