import requests
import json
import time

# 配置区域 (需替换为真实的飞书应用凭证)
APP_ID = "cli_a1b2c3d4e5"
APP_SECRET = "your_app_secret_here"
VIP_GROUP_ID = "g_12345678"  # "付费会员"用户组ID
MEMBER_BITABLE_TOKEN = "bascn123456789"  # 会员管理多维表格Token
TABLE_ID = "tbl123456"  # 数据表ID

class FeishuAutomation:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = ""
        self.token_expire_time = 0

    def get_tenant_access_token(self):
        """获取飞书自建应用 Tenant Access Token"""
        if time.time() < self.token_expire_time:
            return self.token

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            if data.get("code") == 0:
                self.token = data["tenant_access_token"]
                self.token_expire_time = time.time() + data["expire"] - 60 # 提前60秒过期
                return self.token
            else:
                print(f"Error getting token: {data}")
                return None
        except Exception as e:
            print(f"Exception getting token: {e}")
            return None

    def add_user_to_group(self, user_id, group_id):
        """
        将用户添加到指定权限组 (赋予知识库访问权限)
        API文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/group-member/create
        """
        token = self.get_tenant_access_token()
        url = f"https://open.feishu.cn/open-apis/contact/v3/groups/{group_id}/members"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "member_type": "user",
            "member_id_type": "user_id", # 或 open_id
            "member_id": user_id
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if data.get("code") == 0:
            print(f"Success: User {user_id} added to Group {group_id}")
            return True
        else:
            print(f"Failed to add user to group: {data}")
            return False

    def add_member_record(self, user_info):
        """
        在多维表格中创建会员档案
        API文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create
        """
        token = self.get_tenant_access_token()
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{MEMBER_BITABLE_TOKEN}/tables/{TABLE_ID}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 假设多维表格字段: 姓名, 手机号, 会员等级, 到期时间
        fields = {
            "姓名": user_info.get("name"),
            "手机号": user_info.get("phone"),
            "会员等级": "VIP",
            "入会时间": int(time.time() * 1000), # 毫秒级时间戳
            "到期时间": int((time.time() + 365*24*3600) * 1000) # 一年后
        }
        
        payload = {"fields": fields}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if data.get("code") == 0:
            print(f"Success: Member record created for {user_info.get('name')}")
            return True
        else:
            print(f"Failed to create record: {data}")
            return False

    def send_welcome_message(self, user_id):
        """发送欢迎卡片消息"""
        token = self.get_tenant_access_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 简单的文本消息示例，实际建议使用富文本卡片
        content = {
            "text": "🎉 欢迎加入AI自媒体写作变现知识库！\n\n您的会员权限已开通。\n请点击链接开始学习：https://your-knowledge-base-url.feishu.cn/wiki/"
        }
        
        payload = {
            "receive_id": user_id,
            "msg_type": "text",
            "content": json.dumps(content)
        }
        
        params = {"receive_id_type": "user_id"}
        
        requests.post(url, headers=headers, params=params, json=payload)

# 模拟业务流程：当支付回调被触发时调用
def on_payment_success(user_id, user_name, user_phone):
    bot = FeishuAutomation(APP_ID, APP_SECRET)
    
    print(f"Processing new member: {user_name}")
    
    # 1. 开通权限 (加入知识库可见组)
    bot.add_user_to_group(user_id, VIP_GROUP_ID)
    
    # 2. 登记档案 (写入多维表格)
    bot.add_member_record({
        "name": user_name,
        "phone": user_phone
    })
    
    # 3. 发送通知
    bot.send_welcome_message(user_id)

if __name__ == "__main__":
    # 模拟测试数据
    test_user_id = "ou_fake123456"
    test_name = "张三"
    test_phone = "13800138000"
    
    # 注意：直接运行会报错，因为APP_ID和Secret是假的
    print("Starting simulation...")
    # on_payment_success(test_user_id, test_name, test_phone)
    print("Simulation code ready. Please fill in real credentials.")
