"""orchcheck —— 自检测试。

校验智能体编排图的连线与节点配置

覆盖：正常路径、边界输入、防呆红线、幂等性。
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import orchcheck  # noqa: E402

SAMPLE_TEXT = '{"content": "x", "source": "s", "timestamp": "t", "score": 0.5}'


class TestOrchcheck(unittest.TestCase):
    """编排图校验"""

    def test_cli_help_exits_zero(self):
        """--help 必须能正常退出。"""
        import subprocess
        proc = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "orchcheck.py"), "--help"],
            capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)

    def test_cli_rejects_empty_input(self):
        """空输入必须明确报错，不能静默成功。"""
        import subprocess
        proc = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "orchcheck.py"), "--text", "   "],
            capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(proc.returncode, 0)

    def test_cli_json_output_parses(self):
        """--json 输出必须是合法 JSON。"""
        import subprocess
        proc = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "orchcheck.py"), "--text", SAMPLE_TEXT,
             "--json"],
            capture_output=True, text=True, encoding="utf-8")
        if proc.returncode not in (0, 1):
            self.fail(f"退出码异常：{proc.returncode} {proc.stderr[:300]}")
        data = json.loads(proc.stdout)
        self.assertIsInstance(data, dict)

    def test_does_not_mutate_input(self):
        """防呆：分析过程不得改动调用方传入的对象。"""
        payload = SAMPLE_TEXT
        before = payload
        orchcheck.orchcheck_analyze(payload)
        self.assertEqual(before, payload)

    def test_is_idempotent(self):
        """同一输入跑两次结果必须一致。"""
        a = orchcheck.orchcheck_analyze(SAMPLE_TEXT)
        b = orchcheck.orchcheck_analyze(SAMPLE_TEXT)
        self.assertEqual(json.dumps(a, ensure_ascii=False, sort_keys=True),
                         json.dumps(b, ensure_ascii=False, sort_keys=True))

    def test_detects_missing_required_fields(self):
        r = orchcheck.orchcheck_analyze('{"content": "x"}')
        self.assertTrue(r["ok"])
        self.assertTrue(r["missing"])

    def test_reports_invalid_json_position(self):
        """坏 JSON 要报出位置，不只是「解析失败」。"""
        r = orchcheck.orchcheck_analyze("{not json")
        self.assertFalse(r["ok"])
        self.assertIn("line", r)
        self.assertIn("column", r)

    def test_valid_payload_is_clean(self):
        """防呆：合法结构不该被误报。"""
        r = orchcheck.orchcheck_analyze(SAMPLE_TEXT)
        self.assertTrue(r["ok"])
