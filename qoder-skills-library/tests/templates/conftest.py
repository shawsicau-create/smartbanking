"""
技能测试配置文件
提供测试夹具和配置
"""
import pytest
from pathlib import Path


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--skill-path",
        action="append",
        default=[],
        help="技能目录路径"
    )


@pytest.fixture
def skill_path(request):
    """技能路径夹具"""
    return Path(request.param)


@pytest.fixture
def skill_name(skill_path):
    """技能名称夹具"""
    return skill_path.name


@pytest.fixture
def skill_md_path(skill_path):
    """SKILL.md文件路径夹具"""
    return skill_path / "SKILL.md"


@pytest.fixture
def skill_content(skill_md_path):
    """SKILL.md文件内容夹具"""
    return skill_md_path.read_text(encoding='utf-8')


@pytest.fixture
def skill_frontmatter(skill_content):
    """技能前置数据夹具"""
    import yaml
    parts = skill_content.split('---', 2)
    if len(parts) >= 3:
        return yaml.safe_load(parts[1])
    return {}


@pytest.fixture
def skill_body(skill_content):
    """技能正文内容夹具"""
    parts = skill_content.split('---', 2)
    if len(parts) >= 3:
        return parts[2].strip()
    return ""


def pytest_collection_modifyitems(config, items):
    """修改测试项收集"""
    # 如果没有指定技能路径，跳过所有测试
    if not config.getoption("--skill-path"):
        skip_marker = pytest.mark.skip(reason="需要指定 --skill-path 选项")
        for item in items:
            item.add_marker(skip_marker)
