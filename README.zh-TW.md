# MCP 汎宇電商電子發票伺服器

[MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 伺服器，封裝 **汎宇電商 (Universal EC) 台灣電子發票 POS 機 Web Service** (JSON 格式, MIG4.1)。透過 stdio JSON-RPC 2.0 提供 27 個 AI 可呼叫的工具，涵蓋所有可用的功能代碼。

[English](README.md)

## 功能特色

- **27 個 MCP 工具** — 完整涵蓋汎宇電商電子發票 API 所有功能代碼
- **stdio JSON-RPC 2.0** — 標準 MCP 傳輸協定
- **3 種封裝格式** — INDEX、Invoice、Allowance（依功能自動選擇）
- **憑證自動注入** — SELLERID/POSID/POSSN 由 connector 自動注入
- **TDD 測試** — 53 個單元測試 + 5 個即時回歸測試

## 快速開始

```bash
# 安裝
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# 設定憑證
cp .env.example .env
# 編輯 .env 填入你的汎宇電商憑證

# 啟動伺服器
python mcp_server.py
```

## 設定

建立 `.env` 檔案，填入汎宇電商 POS 機憑證：

```
EINVOICE_BASE_URL=https://epostw.einvoice.com.tw/GetInvoice.ashx
EINVOICE_SELLER_ID=your_seller_id
EINVOICE_POS_ID=your_pos_id
EINVOICE_POS_SN=your_pos_sn
```

| 環境 | URL |
|---|---|
| 測試機 | `https://epostw.einvoice.com.tw/GetInvoice.ashx` |
| 正式機 | `https://eposw.einvoice.com.tw/GetInvoice.ashx` |

## 專案結構

```
mcp-universalec-e-invoice/
├── app.py                          # FastMCP 單例
├── mcp_server.py                   # 進入點 (stdio 傳輸)
├── config/
│   └── settings.py                 # URL + 憑證 (從 .env 讀取)
├── connectors/
│   └── einvoice_client.py          # 單一 POST 連接器 (3 種封裝格式)
├── tools/
│   ├── system_tools.py             # Y01
│   ├── invoice_number_tools.py     # A01, C01, Z21, Z22
│   ├── b2c_invoice_tools.py        # C0401, C0401N, C0501
│   ├── b2b_invoice_tools.py        # A0401, A0501, A0101, A0201
│   ├── allowance_tools.py          # D0401, D0401N, D0501, B0401, B0501, B0101
│   ├── cancel_tools.py             # C0701, B0701
│   ├── query_tools.py              # Z11, Z31, Z33, Z34
│   └── admin_tools.py              # Z32, E0401, E0402
└── tests/
    ├── conftest.py                 # 共用 fixtures
    ├── test_einvoice_client.py     # 連接器單元測試
    ├── test_system_tools.py        # Y01 測試
    ├── test_invoice_number_tools.py
    ├── test_b2c_invoice_tools.py
    ├── test_b2b_invoice_tools.py
    ├── test_allowance_tools.py
    ├── test_cancel_tools.py
    ├── test_query_tools.py
    ├── test_admin_tools.py
    └── test_regression.py          # 即時 API 測試
```

## 工具列表 (27 個)

### 系統
| 工具 | 代碼 | 說明 |
|---|---|---|
| `get_system_time` | Y01 | 連線測試 / 取得伺服器時間 |

### 發票號碼管理
| 工具 | 代碼 | 說明 |
|---|---|---|
| `get_invoice_numbers` | A01 | 取得發票號碼配號（本期） |
| `get_next_period_numbers` | C01 | 取得發票號碼配號（下期） |
| `get_invoice_numbers_expanded` | Z21 | 展開取號含 AESKEY（本期） |
| `get_next_period_numbers_expanded` | Z22 | 展開取號含 AESKEY（下期） |

### B2C 發票
| 工具 | 代碼 | 說明 |
|---|---|---|
| `create_b2c_invoice` | C0401 | 開立 B2C 發票（位置欄位格式） |
| `create_b2c_invoice_named` | C0401N | 開立 B2C 發票（命名欄位格式） |
| `void_b2c_invoice` | C0501 | 作廢 B2C 發票 |

### B2B 發票
| 工具 | 代碼 | 說明 |
|---|---|---|
| `create_b2b_invoice` | A0401 | 開立 B2B 發票（平台存證） |
| `void_b2b_invoice` | A0501 | 作廢 B2B 發票 |
| `create_b2b_exchange_invoice` | A0101 | 開立 B2B 交換發票 |
| `void_b2b_exchange_invoice` | A0201 | 作廢 B2B 交換發票 |

### 折讓
| 工具 | 代碼 | 說明 |
|---|---|---|
| `create_b2c_allowance` | D0401 | 開立 B2C 折讓證明單 |
| `create_b2c_allowance_named` | D0401N | 開立 B2C 折讓（命名格式） |
| `void_b2c_allowance` | D0501 | 作廢 B2C 折讓證明單 |
| `create_b2b_allowance` | B0401 | 開立 B2B 折讓證明單 |
| `void_b2b_allowance` | B0501 | 作廢 B2B 折讓證明單 |
| `create_b2b_exchange_allowance` | B0101 | 開立 B2B 交換折讓證明單 |

### 註銷
| 工具 | 代碼 | 說明 |
|---|---|---|
| `cancel_invoice` | C0701 | 註銷發票 |
| `batch_cancel_invoice` | B0701 | 批次註銷（含完整發票資料） |

### 查詢
| 工具 | 代碼 | 說明 |
|---|---|---|
| `get_cancel_status` | Z11 | 查詢發票註銷流程狀態 |
| `get_downloaded_track_ranges` | Z31 | 查詢已下載字軌區間 |
| `get_assignment_info` | Z33 | 查詢統編配號（自動/手動） |
| `get_winning_list` | Z34 | 下載中獎清冊 |

### 管理
| 工具 | 代碼 | 說明 |
|---|---|---|
| `upload_next_period_tracks` | Z32 | 上傳下期字軌配號 |
| `assign_branch_tracks` | E0401 | 分支機構配號 |
| `report_unused_tracks` | E0402 | 空白未使用字軌回報 |

## 測試

```bash
# 單元測試（模擬 HTTP，不需要憑證）
pytest tests/ --ignore=tests/test_regression.py -v

# 回歸測試（需要 .env 中的有效憑證）
pytest tests/test_regression.py -v -s
```

## 架構

所有 27 個功能透過單一 POST 端點 (`GetInvoice.ashx`) 通訊，以 JSON body 中的功能代碼區分。連接器自動注入憑證 (SELLERID, POSID, POSSN) 與系統時間。

三種 JSON 封裝格式：
- **INDEX** — 系統/號碼功能 (Y01, A01, C01, Z21, Z22, Z11)
- **Invoice** — 發票/折讓/管理 CRUD (C0401, A0401, D0401, C0701, E0401, Z31 等)
- **Allowance** — 僅 B0501（作廢 B2B 折讓）

## 授權

MIT License — 詳見 [LICENSE](LICENSE)。
