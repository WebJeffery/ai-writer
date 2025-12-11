# AI自媒体写作变现知识库 - 设计方案

本项目包含构建一个基于飞书（Lark）平台的付费知识库所需的完整设计文档和技术实现方案。

## 📂 交付物清单

| 模块 | 文件路径 | 说明 |
| :--- | :--- | :--- |
| **1. 知识库架构** | `docs/1_Knowledge_Base_Structure.md` | 包含目录树设计、三级体系（基础/进阶/实战）及单页面内容标准。 |
| **2. 权限与安全** | `docs/2_Permission_and_Security.md` | 详细的付费隔离方案、权限组配置及防盗版水印设置。 |
| **3. 运营SOP** | `docs/3_Operations_SOP.md` | 涵盖学员入群、作业批改、直播答疑的标准作业程序。 |
| **4. 自动化脚本** | `src/membership_automation.py` | Python脚本示例，演示如何对接飞书API实现自动开通会员权限。 |

## 🚀 快速开始

### 第一步：搭建知识库
按照 `docs/1_Knowledge_Base_Structure.md` 中的目录结构，在飞书知识库中创建对应页面。建议使用“文档”而非“旧版文档”，以支持更丰富的组件。

### 第二步：配置权限
参考 `docs/2_Permission_and_Security.md`，在飞书管理后台创建 `VIP_Members` 用户组，并对知识库的不同章节设置“仅该组成员可见”。

### 第三步：部署自动化
1. 在飞书开放平台 (open.feishu.cn) 创建企业自建应用。
2. 开通以下权限：
   - 通讯录 (Contact): `contact:group.member:readonly`, `contact:group.member:write`
   - 消息 (Message): `im:message:send`
   - 多维表格 (Bitable): `bitable:app:read`, `bitable:record:write`
3. 修改 `src/membership_automation.py` 中的 `APP_ID` 和 `APP_SECRET`。
4. 将脚本部署到你的服务器或云函数（如阿里云FC），并配置支付回调触发该脚本。

## 💡 核心亮点
- **阶梯式解锁**：通过权限组动态管理实现内容分层。
- **自动化运营**：支付即开通，减少人工拉群成本。
- **全链路闭环**：从引流（试读）到转化（付费）再到留存（督导）的完整设计。
