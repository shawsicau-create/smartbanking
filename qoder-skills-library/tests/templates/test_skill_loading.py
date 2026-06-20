"""
技能加载测试模板
用于验证SKILL.md文件的基本结构和内容
"""
import pytest
import yaml
from pathlib import Path


class TestSkillLoading:
    """技能加载测试类"""
    
    def test_skill_directory_exists(self, skill_path):
        """测试技能目录是否存在"""
        assert skill_path.exists(), f"技能目录不存在: {skill_path}"
        assert skill_path.is_dir(), f"路径不是目录: {skill_path}"
    
    def test_skill_md_exists(self, skill_path):
        """测试SKILL.md文件是否存在"""
        skill_md = skill_path / "SKILL.md"
        assert skill_md.exists(), f"SKILL.md文件不存在: {skill_md}"
    
    def test_skill_md_has_frontmatter(self, skill_path):
        """测试SKILL.md文件是否包含YAML前置数据"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 检查是否以---开头
        assert content.startswith('---'), "SKILL.md文件应以---开头"
        
        # 提取前置数据
        parts = content.split('---', 2)
        assert len(parts) >= 3, "SKILL.md文件格式错误，应包含前置数据和正文"
        
        frontmatter = parts[1]
        try:
            data = yaml.safe_load(frontmatter)
            assert isinstance(data, dict), "前置数据应为字典格式"
        except yaml.YAMLError as e:
            pytest.fail(f"前置数据YAML格式错误: {e}")
    
    def test_skill_md_has_required_fields(self, skill_path):
        """测试SKILL.md文件是否包含必需字段"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查必需字段
        required_fields = ['name', 'description', 'workflow_stage', 'compatibility', 'author', 'version', 'tags']
        for field in required_fields:
            assert field in data, f"缺少必需字段: {field}"
    
    def test_skill_name_matches_directory(self, skill_path):
        """测试技能名称是否与目录名称匹配"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查名称匹配
        expected_name = skill_path.name
        actual_name = data.get('name')
        assert actual_name == expected_name, f"技能名称不匹配: 期望 '{expected_name}', 实际 '{actual_name}'"
    
    def test_skill_has_valid_workflow_stage(self, skill_path):
        """测试技能是否有有效的工作流阶段"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查工作流阶段
        valid_stages = ['ideation', 'literature', 'theory', 'data', 'analysis', 'writing', 'communication', 'engineering']
        workflow_stage = data.get('workflow_stage')
        assert workflow_stage in valid_stages, f"无效的工作流阶段: {workflow_stage}"
    
    def test_skill_has_valid_compatibility(self, skill_path):
        """测试技能是否有有效的兼容性列表"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查兼容性
        compatibility = data.get('compatibility')
        assert isinstance(compatibility, list), "兼容性应为列表格式"
        assert len(compatibility) > 0, "兼容性列表不能为空"
        
        # 检查有效的兼容性平台
        valid_platforms = ['claude-code', 'cursor', 'codex', 'gemini-cli']
        for platform in compatibility:
            assert platform in valid_platforms, f"无效的兼容性平台: {platform}"
    
    def test_skill_has_valid_version(self, skill_path):
        """测试技能是否有有效的版本号"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查版本号
        version = data.get('version')
        assert isinstance(version, str), "版本号应为字符串格式"
        
        # 简单的版本号格式检查
        import re
        assert re.match(r'^\d+\.\d+\.\d+$', version), f"版本号格式无效: {version}"
    
    def test_skill_has_tags(self, skill_path):
        """测试技能是否有标签"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查标签
        tags = data.get('tags')
        assert isinstance(tags, list), "标签应为列表格式"
        assert len(tags) > 0, "标签列表不能为空"
        
        # 检查标签格式
        for tag in tags:
            assert isinstance(tag, str), "标签应为字符串格式"
            assert tag.islower(), f"标签应为小写: {tag}"
    
    def test_skill_has_description(self, skill_path):
        """测试技能是否有描述"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取前置数据
        parts = content.split('---', 2)
        frontmatter = parts[1]
        data = yaml.safe_load(frontmatter)
        
        # 检查描述
        description = data.get('description')
        assert isinstance(description, str), "描述应为字符串格式"
        assert len(description) > 0, "描述不能为空"
        assert len(description) <= 100, "描述长度不应超过100个字符"
    
    def test_skill_has_body_content(self, skill_path):
        """测试技能是否有正文内容"""
        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text(encoding='utf-8')
        
        # 提取正文
        parts = content.split('---', 2)
        body = parts[2].strip()
        
        # 检查正文内容
        assert len(body) > 0, "技能正文内容不能为空"
        assert len(body) > 100, "技能正文内容过短，应至少100个字符"
