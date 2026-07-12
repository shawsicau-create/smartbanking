"""
bank-greeting Skill - 银行欢迎语技能

功能：为银行客户提供个性化的欢迎语和服务指引
"""

from datetime import datetime
from typing import Optional

class BankGreetingSkill:
    """
    银行欢迎语技能类
    
    提供根据时间、客户等级、节日等条件生成个性化欢迎语的功能
    """
    
    def __init__(self):
        self.greetings = {
            'morning': [
                '早上好！欢迎光临招商银行，今天天气不错，祝您一天好心情！',
                '早安！感谢您选择招商银行，请问有什么可以帮助您的？',
                '早晨好！招商银行竭诚为您服务，期待为您提供优质服务！'
            ],
            'afternoon': [
                '下午好！欢迎来到招商银行，请问需要办理什么业务？',
                '您好！感谢您在百忙之中光临，我们将为您提供专业服务！',
                '下午好！招商银行随时为您服务，祝您生活愉快！'
            ],
            'evening': [
                '晚上好！感谢您今天的光临，祝您晚安！',
                '您好！今天的服务即将结束，如有需要请明天再来！',
                '晚间好！感谢您选择招商银行，祝您度过愉快的夜晚！'
            ]
        }
        
        self.vip_greetings = [
            '尊敬的VIP客户，您好！专属服务通道已为您开启！',
            '尊贵的VIP客户，欢迎回来！我们已为您准备了专属服务！',
            '您好！VIP专属顾问将在一分钟内为您服务！'
        ]
        
        self.festivals = {
            '元旦': '新年好！祝您元旦快乐，万事如意！',
            '春节': '新春快乐！祝您龙年大吉，财源广进！',
            '元宵': '元宵节快乐！祝您团团圆圆，幸福美满！',
            '清明': '清明节安康！愿逝者安息，生者坚强！',
            '五一': '劳动节快乐！祝您假期愉快，劳逸结合！',
            '端午': '端午节安康！祝您身体健康，阖家欢乐！',
            '中秋': '中秋节快乐！祝您月圆人圆，事事圆满！',
            '国庆': '国庆节快乐！祝伟大祖国繁荣昌盛！',
            '圣诞': '圣诞节快乐！愿您拥有美好的一天！',
            '生日': '生日快乐！招商银行祝您年年有今日，岁岁有今朝！'
        }
    
    def get_time_period(self) -> str:
        """获取当前时间段"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        else:
            return 'evening'
    
    def get_today_festival(self) -> Optional[str]:
        """获取今天的节日"""
        today = datetime.now()
        month_day = (today.month, today.day)
        
        festivals_map = {
            (1, 1): '元旦',
            (1, 15): '元宵',
            (4, 4): '清明',
            (5, 1): '五一',
            (6, 22): '端午',
            (9, 17): '中秋',
            (10, 1): '国庆',
            (12, 25): '圣诞'
        }
        
        # 春节日期需要动态计算，这里简化处理
        if month_day == (1, 29):  # 示例日期
            return '春节'
        
        return festivals_map.get(month_day)
    
    def generate_greeting(
        self,
        customer_name: Optional[str] = None,
        customer_level: str = '普通客户',
        is_birthday: bool = False
    ) -> str:
        """
        生成个性化欢迎语
        
        Args:
            customer_name: 客户姓名
            customer_level: 客户等级（普通客户/金卡客户/VIP客户）
            is_birthday: 是否是客户生日
        
        Returns:
            个性化欢迎语
        """
        import random
        
        # 生日祝福优先
        if is_birthday:
            greeting = self.festivals['生日']
            if customer_name:
                greeting = f'{customer_name}先生/女士，{greeting}'
            return greeting
        
        # 节日祝福
        festival = self.get_today_festival()
        if festival:
            return self.festivals[festival]
        
        # VIP客户专属问候
        if customer_level in ['金卡客户', 'VIP客户']:
            greeting = random.choice(self.vip_greetings)
            if customer_name:
                greeting = greeting.replace('尊贵的', f'尊敬的{customer_name}')
            return greeting
        
        # 根据时间生成问候
        time_period = self.get_time_period()
        greeting = random.choice(self.greetings[time_period])
        
        # 添加客户姓名
        if customer_name:
            greeting = f'{customer_name}先生/女士，{greeting}'
        
        return greeting
    
    def generate_service_guide(self, service_type: str = None) -> str:
        """
        生成服务指引
        
        Args:
            service_type: 服务类型
        
        Returns:
            服务指引信息
        """
        guides = {
            '开户': '如需办理开户业务，请前往1号窗口，需要携带身份证原件。',
            '理财': '理财咨询请前往理财专区，专业理财顾问将为您服务。',
            '贷款': '贷款业务咨询请前往2号窗口，我们提供多种贷款产品。',
            '挂失': '如需挂失服务，请立即拨打紧急热线：95555。',
            '转账': '转账业务可以通过ATM机或手机银行办理，更加便捷。'
        }
        
        if service_type and service_type in guides:
            return guides[service_type]
        
        return (
            '如需帮助，您可以：\n'
            '1. 前往咨询台获取服务指引\n'
            '2. 使用大厅自助终端办理业务\n'
            '3. 下载招商银行APP享受便捷服务\n'
            '4. 拨打客服热线：95555'
        )

# Skill注册配置
SKILL_CONFIG = {
    'name': 'bank-greeting',
    'description': '银行欢迎语技能，为客户提供个性化问候服务',
    'version': '1.0.0',
    'author': '招商银行科技开发部',
    'entry_point': 'BankGreetingSkill',
    'requirements': [],
    'capabilities': [
        {
            'name': 'generate_greeting',
            'description': '生成个性化欢迎语',
            'parameters': [
                {'name': 'customer_name', 'type': 'string', 'optional': True},
                {'name': 'customer_level', 'type': 'string', 'optional': True},
                {'name': 'is_birthday', 'type': 'bool', 'optional': True}
            ]
        },
        {
            'name': 'generate_service_guide',
            'description': '生成服务指引',
            'parameters': [
                {'name': 'service_type', 'type': 'string', 'optional': True}
            ]
        }
    ],
    'security': {
        'requires_authentication': False,
        'data_protection': 'none'
    }
}

# 测试示例
if __name__ == '__main__':
    skill = BankGreetingSkill()
    
    # 测试普通客户问候
    print('普通客户问候:', skill.generate_greeting('张三', '普通客户'))
    
    # 测试VIP客户问候
    print('VIP客户问候:', skill.generate_greeting('李四', 'VIP客户'))
    
    # 测试生日祝福
    print('生日祝福:', skill.generate_greeting('王五', '金卡客户', is_birthday=True))
    
    # 测试服务指引
    print('服务指引:', skill.generate_service_guide('理财'))