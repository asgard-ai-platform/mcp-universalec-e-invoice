# MCP 汎宇電商電子發票伺服器

[![PyPI version](https://img.shields.io/pypi/v/mcp-universalec-e-invoice)](https://pypi.org/project/mcp-universalec-e-invoice/)
[![Python versions](https://img.shields.io/pypi/pyversions/mcp-universalec-e-invoice)](https://pypi.org/project/mcp-universalec-e-invoice/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md)

開源 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 伺服器，封裝 **汎宇電商 (Universal EC) 台灣電子發票 POS 機 Web Service** (JSON 格式, MIG4.1)。透過 stdio JSON-RPC 2.0 提供 27 個 AI 可呼叫的工具，涵蓋所有可用的功能代碼。

專為 [Claude Code](https://claude.ai/code) 及所有 MCP 相容的 AI 客戶端打造。讓 AI 代理人透過自然語言開立發票、作廢發票、管理發票號碼、查詢註銷狀態、處理折讓。

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

## 使用範例

MCP 伺服器啟動後，AI 助手（如 Claude）可以代你呼叫這些工具。以下是實際使用情境，展示你怎麼說、AI 怎麼做。

---

### 「幫我測試電子發票系統有沒有連線成功」

**AI 呼叫:** `get_system_time()`

**結果:** 系統回傳 `REPLY: "1"`、`MESSAGE: "連線成功"`，伺服器時間 `2026/04/01 22:29:03`。連線正常。

---

### 「我目前有哪些可用的發票號碼？」

**AI 呼叫:** `get_invoice_numbers()`

**結果:** 本期 115 年 03-04 月，字軌 `GS`，號碼 `82775400` ~ `82775449`（共 50 張可用）。AI 同時會說明回傳的 QRCode AES 金鑰用途。

---

### 「我需要取得每張發票的 AESKEY 跟隨機碼，準備列印用」

**AI 呼叫:** `get_invoice_numbers_expanded()`

**結果:** 回傳 50 張發票的個別資訊：
```
GS82775450 → AESKEY: Xymp9aqy..., 隨機碼: 7833
GS82775451 → AESKEY: XausdWBO..., 隨機碼: 4581
...
```

---

### 「幫我開一張發票，客人買了 2 杯拿鐵 65 元、1 個蛋糕 85 元」

**AI 先呼叫** `get_invoice_numbers_expanded()` 取得可用號碼，再呼叫：

```
create_b2c_invoice(
  invoice_number = "GS82775402",     ← 從配號取得
  invoice_date   = "2026-04-01",
  invoice_time   = "14:30:00",
  buyer_id       = "0000000000",     ← 消費者，無統編
  buyer_name     = "0000",
  invoice_type   = "07",
  donate_mark    = "0",
  print_mark     = "Y",
  random_number  = "6136",           ← 從配號取得
  tax_type = "1", tax_rate = "0.05", tax_amount = "10",
  sales_amount = "205", free_tax = "0", zero_tax = "0", total = "215",
  items = [
    {B1:"1", B2:"拿鐵咖啡", B3:"2", B5:"65", B6:"130", B7:"1", B13:"1"},
    {B1:"2", B2:"巧克力蛋糕", B3:"1", B5:"85", B6:"85", B7:"2", B13:"1"},
  ]
)
```

**結果:** `REPLY: "1"`，`MESSAGE: "成功"`，發票 `GS82775402` 開立完成。

---

### 「請幫我作廢發票 GS82775401，客戶取消訂單」

**AI 呼叫:**
```
void_b2c_invoice(
  invoice_number = "GS82775401",
  invoice_date   = "2026-04-01",
  buyer_id       = "0000000000",
  seller_id      = "23997652",
  cancel_date    = "2026-04-01",
  cancel_time    = "15:00:00",
  cancel_reason  = "客戶取消訂單",
)
```

**結果:** `REPLY: "1"`，`MESSAGE: "成功"` — 發票作廢成功。

---

### 「幫我查一下 GS82775400 的註銷狀態」

**AI 呼叫:** `get_cancel_status(invoice_number="GS82775400", invoice_date="2026-04-01")`

**結果:** `STATUSCODE: "1"` = 已完成、`"2"` = 尚未完成、`"3"` = 失敗。AI 會用白話告訴你目前狀態。

---

### 「發票 GS82775400 開錯了，幫我註銷」

**AI 呼叫:**
```
cancel_invoice(
  invoice_number = "GS82775400",
  invoice_date   = "2026-04-01",
  buyer_id       = "0000000000",
  seller_id      = "23997652",
  cancel_date    = "2026-04-01",
  cancel_time    = "16:00:00",
  cancel_reason  = "誤開發票",
)
```

**結果:** 若發票已上傳財政部，`REPLY: "1"` 表示註銷成功。若尚未上傳，系統回傳 `REPLY: "-1"` 說明發票仍在處理中 — AI 會告訴你稍後再試。

> **備註：**「作廢」(C0501) 和「註銷」(C0701) 不同。作廢是發票尚未上傳財政部前的操作；註銷是上傳後的操作。AI 會根據情境自動選擇正確的工具。

---

### 「查一下這期 GS 字軌已下載的配號區間」

**AI 呼叫:**
```
get_downloaded_track_ranges(
  head_ban      = "23997652",
  branch_ban    = "23997652",
  invoice_type  = "07",
  year_month    = "11504",
  invoice_track = "GS",
)
```

**結果:** 回傳該期別已成功下載的字軌區間明細。

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
