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

## 使用範例

以下範例皆經過汎宇電商測試環境實測驗證。

### 範例 1：連線測試 (Y01)

```python
from tools.system_tools import get_system_time

result = get_system_time()
# 回應:
# {
#   "INDEX": {
#     "FUNCTIONCODE": "Y01",
#     "REPLY": "1",
#     "MESSAGE": "連線成功",
#     "SYSTIME": "2026/04/01 22:29:03"
#   }
# }
```

### 範例 2：取得發票號碼 (A01)

```python
from tools.invoice_number_tools import get_invoice_numbers

result = get_invoice_numbers()
# 回應:
# {
#   "INDEX": {
#     "REPLY": "1",
#     "TAXMONTH": "11504",          ← 發票期別（民國 115 年 03-04 月）
#     "INVOICEHEADER": "GS",        ← 發票字軌
#     "INVOICESTART": "82775400",   ← 起始號碼
#     "INVOICEEND": "82775449",     ← 結束號碼（共 50 張）
#     "QRCodeASKey": "D016F2FF..."  ← QR Code 加密金鑰
#   }
# }
```

### 範例 3：展開取號含 AESKEY (Z21)

每張發票取得獨立的 AESKEY 與隨機碼，供 QR Code 產生使用。

```python
from tools.invoice_number_tools import get_invoice_numbers_expanded

result = get_invoice_numbers_expanded()
# INVOICEDATA 陣列包含每張發票的資訊:
# [
#   {"INVOICE_NUMBER": "GS82775450", "AESKEY": "Xymp9aqy...", "RANDOMNUMBER": "7833"},
#   {"INVOICE_NUMBER": "GS82775451", "AESKEY": "XausdWBO...", "RANDOMNUMBER": "4581"},
#   ...
# ]
```

### 範例 4：開立 B2C 發票 (C0401)

```python
from tools.b2c_invoice_tools import create_b2c_invoice

result = create_b2c_invoice(
    invoice_number="GS82775401",
    invoice_date="2026-04-01",
    invoice_time="22:35:00",
    buyer_id="0000000000",       # 消費者（無統編）
    buyer_name="0000",           # 系統自動轉換為 4 碼隨機數
    invoice_type="07",
    donate_mark="0",             # 非捐贈
    print_mark="Y",              # 已列印紙本
    random_number="5678",
    tax_type="1",                # 應稅
    tax_rate="0.05",
    tax_amount="5",
    sales_amount="95",
    free_tax="0",
    zero_tax="0",
    total="100",
    items=[
        {"B1": "1", "B2": "美式咖啡", "B3": "2", "B5": "50", "B6": "100", "B7": "1", "B13": "1"},
    ],
)
# REPLY: "1", MESSAGE: "成功", ERROR_CODE: "0000"
```

### 範例 5：作廢發票 (C0501)

```python
from tools.b2c_invoice_tools import void_b2c_invoice

result = void_b2c_invoice(
    invoice_number="GS82775401",
    invoice_date="2026-04-01",
    buyer_id="0000000000",
    seller_id="23997652",
    cancel_date="2026-04-01",
    cancel_time="22:36:00",
    cancel_reason="測試作廢",
)
# REPLY: "1", MESSAGE: "成功"
```

### 範例 6：查詢註銷狀態 (Z11)

```python
from tools.query_tools import get_cancel_status

result = get_cancel_status(
    invoice_number="GS82775400",
    invoice_date="2026-04-01",
)
# STATUSCODE: "1"=已完成, "2"=尚未完成, "3"=失敗
```

### 範例 7：完整流程 — 取號、開票、作廢

```python
from tools.invoice_number_tools import get_invoice_numbers_expanded
from tools.b2c_invoice_tools import create_b2c_invoice, void_b2c_invoice

# 第一步：取得可用發票號碼（含 AESKEY）
numbers = get_invoice_numbers_expanded()
inv = numbers["INDEX"]["INVOICEDATA"][0]

# 第二步：使用配號開立發票
result = create_b2c_invoice(
    invoice_number=inv["INVOICE_NUMBER"],
    invoice_date="2026-04-01",
    invoice_time="14:30:00",
    buyer_id="0000000000",
    buyer_name="0000",
    invoice_type="07",
    donate_mark="0",
    print_mark="Y",
    random_number=inv["RANDOMNUMBER"],
    tax_type="1", tax_rate="0.05", tax_amount="10",
    sales_amount="190", free_tax="0", zero_tax="0", total="200",
    items=[
        {"B1": "1", "B2": "拿鐵咖啡", "B3": "2", "B5": "65", "B6": "130", "B7": "1", "B13": "1"},
        {"B1": "2", "B2": "巧克力蛋糕", "B3": "1", "B5": "70", "B6": "70", "B7": "2", "B13": "1"},
    ],
)
assert result["INDEX"]["REPLY"] == "1"

# 第三步：如需作廢
void_result = void_b2c_invoice(
    invoice_number=inv["INVOICE_NUMBER"],
    invoice_date="2026-04-01",
    buyer_id="0000000000",
    seller_id="23997652",
    cancel_date="2026-04-01",
    cancel_time="15:00:00",
    cancel_reason="客戶取消訂單",
)
assert void_result["INDEX"]["REPLY"] == "1"
```

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
