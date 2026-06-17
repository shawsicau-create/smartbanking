#!/usr/bin/env python3
"""
error_handling.py - 友好的错误提示和处理

P1-5: 友好的错误提示 - 提升用户体验，降低挫败感

功能：
  - 统一的错误消息格式
  - 可操作的解决建议
  - 错误分类和日志记录
  - 支持中英文错误消息

使用示例：
    from scripts.error_handling import (
        SLRError, handle_error, friendly_exception_handler
    )

    # 方式1: 抛出带建议的错误
    raise SLRError(
        message="API调用失败",
        suggestions=[
            "检查网络连接",
            "稍后重试（可能达到速率限制）",
            "使用 --offline 模式生成检索方案"
        ],
        error_code="API_001"
    )

    # 方式2: 使用装饰器
    @friendly_exception_handler
    def risky_function():
        ...

    # 方式3: 手动处理
    try:
        ...
    except Exception as e:
        handle_error(e, context={"api": "Semantic Scholar"})
"""

import functools
import logging
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Callable

logger = logging.getLogger(__name__)


# ============================================================================
# 错误分类
# ============================================================================

class ErrorCode(Enum):
    """错误代码枚举"""
    # API 相关
    API_TIMEOUT = "API_001"
    API_RATE_LIMIT = "API_002"
    API_CONNECTION_ERROR = "API_003"
    API_AUTH_ERROR = "API_004"

    # 文件相关
    FILE_NOT_FOUND = "FILE_001"
    FILE_FORMAT_ERROR = "FILE_002"
    FILE_PERMISSION_ERROR = "FILE_003"

    # 配置相关
    CONFIG_ERROR = "CONFIG_001"
    CONFIG_MISSING_FIELD = "CONFIG_002"

    # 检索相关
    SEARCH_NO_RESULTS = "SEARCH_001"
    SEARCH_ENGINE_UNAVAILABLE = "SEARCH_002"

    # 数据相关
    DATA_VALIDATION_ERROR = "DATA_001"
    DATA_MISSING_FIELD = "DATA_002"

    # 通用错误
    UNKNOWN_ERROR = "GEN_001"


# ============================================================================
# 自定义错误类
# ============================================================================

class SLRError(Exception):
    """系统综述技能基础错误类"""

    def __init__(
        self,
        message: str,
        suggestions: Optional[List[str]] = None,
        error_code: Optional[ErrorCode] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        初始化错误

        Args:
            message: 错误消息
            suggestions: 解决建议列表
            error_code: 错误代码
            context: 错误上下文信息
        """
        self.message = message
        self.suggestions = suggestions or []
        self.error_code = error_code or ErrorCode.UNKNOWN_ERROR
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self):
        """友好的错误消息格式"""
        lines = [
            "\n" + "=" * 60,
            f"❌ 错误: {self.message}",
            "=" * 60
        ]

        # 错误代码
        lines.append(f"错误代码: {self.error_code.value}")

        # 上下文信息
        if self.context:
            lines.append("\n上下文信息:")
            for key, value in self.context.items():
                lines.append(f"  - {key}: {value}")

        # 解决建议
        if self.suggestions:
            lines.append("\n💡 可能的解决方案:")
            for i, suggestion in enumerate(self.suggestions, 1):
                lines.append(f"  {i}. {suggestion}")

        lines.append("=" * 60 + "\n")

        return "\n".join(lines)


# ============================================================================
# 特定错误类
# ============================================================================

class APIError(SLRError):
    """API 调用错误"""

    def __init__(self, api_name: str, original_error: Exception,
                 retry_possible: bool = True):
        suggestions = [
            f"检查 {api_name} 服务状态",
            "检查网络连接",
        ]
        if retry_possible:
            suggestions.extend([
                "稍后重试（可能达到速率限制）",
                "增加请求间隔时间"
            ])
        else:
            suggestions.append("使用其他数据源或离线模式")

        super().__init__(
            message=f"{api_name} API 调用失败: {str(original_error)}",
            suggestions=suggestions,
            error_code=ErrorCode.API_CONNECTION_ERROR,
            context={'api_name': api_name, 'original_error': str(original_error)}
        )


class FileNotFoundError(SLRError):
    """文件未找到错误"""

    def __init__(self, file_path: str, file_type: str = "文件"):
        super().__init__(
            message=f"{file_type}未找到: {file_path}",
            suggestions=[
                f"检查 {file_type}路径是否正确",
                f"确认 {file_type}是否存在",
                "检查文件权限"
            ],
            error_code=ErrorCode.FILE_NOT_FOUND,
            context={'file_path': file_path, 'file_type': file_type}
        )


class ConfigurationError(SLRError):
    """配置错误"""

    def __init__(self, config_path: str, missing_field: str = ""):
        message = f"配置文件错误: {config_path}"
        if missing_field:
            message += f"（缺少字段: {missing_field}）"

        suggestions = [
            "检查 config.yaml 文件是否存在",
            "验证配置文件格式（YAML）",
            "参考 config.yaml.example 示例文件"
        ]
        if missing_field:
            suggestions.insert(0, f"添加缺失字段: {missing_field}")

        super().__init__(
            message=message,
            suggestions=suggestions,
            error_code=ErrorCode.CONFIG_MISSING_FIELD,
            context={'config_path': config_path, 'missing_field': missing_field}
        )


class DataValidationError(SLRError):
    """数据验证错误"""

    def __init__(self, field_name: str, expected_type: str, actual_value: Any):
        super().__init__(
            message=f"数据验证失败: {field_name} 应为 {expected_type}，实际为 {type(actual_value)}",
            suggestions=[
                "检查输入数据格式",
                "参考文档中的数据格式要求",
                "使用验证脚本检查数据"
            ],
            error_code=ErrorCode.DATA_VALIDATION_ERROR,
            context={
                'field_name': field_name,
                'expected_type': expected_type,
                'actual_type': type(actual_value).__name__
            }
        )


# ============================================================================
# 错误处理装饰器
# ============================================================================

def friendly_exception_handler(
    default_message: str = "操作失败",
    reraise: bool = False
):
    """
    友好的异常处理装饰器

    Args:
        default_message: 默认错误消息
        reraise: 是否重新抛出异常

    使用示例:
        @friendly_exception_handler("检索失败")
        def search_papers(query):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SLRError:
                # 已经是友好错误，直接传递
                if reraise:
                    raise
                return None
            except KeyboardInterrupt:
                print("\n\n⚠️  操作被用户中断")
                sys.exit(1)
            except Exception as e:
                # 转换为友好错误
                error = SLRError(
                    message=f"{default_message}: {str(e)}",
                    suggestions=[
                        "检查输入参数",
                        "查看日志获取详细信息",
                        "使用 --verbose 参数获取更多调试信息"
                    ],
                    context={'original_error': str(e)}
                )
                print(error)
                logger.exception(f"未捕获的异常: {e}")

                if reraise:
                    raise
                sys.exit(1)

        return wrapper

    return decorator


# ============================================================================
# 错误处理函数
# ============================================================================

def handle_error(error: Exception, context: Optional[Dict[str, Any]] = None):
    """
    统一错误处理函数

    Args:
        error: 异常对象
        context: 错误上下文

    使用示例:
        try:
            ...
        except Exception as e:
            handle_error(e, context={'api': 'Semantic Scholar'})
    """
    # 已经是 SLRError，直接打印
    if isinstance(error, SLRError):
        if context:
            error.context.update(context)
        print(error)
        logger.error(f"{error.error_code.value}: {error.message}", extra=error.context)
    else:
        # 转换为友好错误
        friendly_error = SLRError(
            message=str(error),
            suggestions=[
                "查看日志获取更多信息",
                "使用 --verbose 参数获取详细调试信息",
                "检查输入参数和数据格式"
            ],
            context=context or {}
        )
        print(friendly_error)

    # 询问用户是否继续
    response = input("\n是否继续执行? (y/n): ").strip().lower()
    if response != 'y':
        print("操作已取消")
        sys.exit(1)


def handle_api_error(api_name: str, error: Exception,
                     retry_count: int = 0, max_retries: int = 3) -> bool:
    """
    处理 API 错误

    Args:
        api_name: API 名称
        error: 异常对象
        retry_count: 当前重试次数
        max_retries: 最大重试次数

    Returns:
        是否应该重试
    """
    error_obj = APIError(api_name, error, retry_count < max_retries)
    print(error_obj)

    if retry_count < max_retries:
        response = input(f"\n是否重试? ({retry_count + 1}/{max_retries}) (y/n): ").strip().lower()
        return response == 'y'
    else:
        print(f"已达到最大重试次数 ({max_retries})")
        return False


# ============================================================================
# 日志配置
# ============================================================================

def setup_logging(verbose: bool = False, log_file: Optional[str] = None):
    """
    配置日志系统

    Args:
        verbose: 是否启用详细日志
        log_file: 日志文件路径
    """
    level = logging.DEBUG if verbose else logging.INFO

    # 配置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # 根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # 文件处理器
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


# ============================================================================
# 上下文管理器
# ============================================================================

class ErrorContext:
    """错误上下文管理器"""

    def __init__(self, operation: str, **context):
        """
        初始化上下文管理器

        Args:
            operation: 操作名称
            **context: 上下文信息
        """
        self.operation = operation
        self.context = context
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"开始操作: {self.operation}", extra=self.context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time

        elapsed = time.time() - self.start_time if self.start_time else 0

        if exc_type is None:
            logger.info(f"操作完成: {self.operation} (用时 {elapsed:.2f}秒)")
            return False

        # 发生错误
        logger.error(
            f"操作失败: {self.operation} (用时 {elapsed:.2f}秒)",
            extra=self.context,
            exc_info=(exc_type, exc_val, exc_tb)
        )

        # 转换为友好错误
        if not isinstance(exc_val, SLRError):
            friendly_error = SLRError(
                message=f"{self.operation} 失败: {str(exc_val)}",
                suggestions=[
                    "查看日志获取更多信息",
                    "检查输入参数"
                ],
                context=self.context
            )
            print(friendly_error)

        # 不抑制异常
        return False


# ============================================================================
# 命令行工具
# ============================================================================

def print_error_summary():
    """打印错误摘要（用于脚本结束时）"""
    print("\n" + "=" * 60)
    print("如遇到问题，请:")
    print("  1. 检查日志文件获取详细信息")
    print("  2. 使用 --verbose 参数重新运行")
    print("  3. 参考文档或提交 Issue")
    print("=" * 60 + "\n")


# ============================================================================
# 示例用法
# ============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='错误处理工具示例')
    parser.add_argument('--demo', choices=['api', 'file', 'config'],
                       default='api', help='演示模式')

    args = parser.parse_args()

    if args.demo == 'api':
        # API 错误演示
        try:
            raise ConnectionError("Connection timeout")
        except Exception as e:
            handle_api_error("Semantic Scholar", e)

    elif args.demo == 'file':
        # 文件错误演示
        raise FileNotFoundError("nonexistent.jsonl", "论文列表文件")

    elif args.demo == 'config':
        # 配置错误演示
        raise ConfigurationError("config.yaml", "quality_thresholds")
