import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from src.clean_junk_logic import JunkFileCleaner
from src.utility import ResourceManager as util


@pytest.fixture
def junk_file_cleaner():
    ui_mock = MagicMock()  # Mock the UI
    return JunkFileCleaner(ui_mock)


# Test for 'find_files_by_pattern'
@patch(
    "pathlib.Path.rglob",
    return_value=[Path("/path/file1.txt"), Path("/path/file2.log")],
)
@patch("pathlib.Path.is_dir", return_value=True)
@patch("pathlib.Path.exists", return_value=True)
def test_find_files_by_pattern(mock_exists, mock_is_dir, mock_rglob, junk_file_cleaner):
    result = junk_file_cleaner.find_files_by_pattern(["/path"], ["*.txt", "*.log"])
    assert sorted(result) == sorted(["/path/file1.txt", "/path/file2.log"])


# Test for 'scan_temp_files'
@patch.object(
    JunkFileCleaner,
    "find_files_by_pattern",
    return_value=["/temp/file1.tmp", "/temp/excluded_app/file2.tmp"],
)
def test_scan_temp_files(mock_find_files, junk_file_cleaner):
    result = junk_file_cleaner.scan_temp_files(["/temp"], ["*.tmp"], ["excluded_app"])
    assert sorted(result) == sorted(["/temp/file1.tmp"])


# Test for 'scan_cache'
@patch.object(
    JunkFileCleaner,
    "find_files_by_pattern",
    return_value=["/cache/file1.cache", "/cache/excluded_app/file2.cache"],
)
def test_scan_cache(mock_find_files, junk_file_cleaner):
    result = junk_file_cleaner.scan_cache(["/cache"], ["*.cache"], ["excluded_app"])
    assert sorted(result) == sorted(["/cache/file1.cache"])


# Test for 'scan_preferences' (fixed the issue)
@patch.object(
    JunkFileCleaner,
    "find_files_by_pattern",
    return_value=["/prefs/file1.plist", "/prefs/excluded_app/file2.plist"],
)
def test_scan_preferences_for_deleted_apps(mock_find_files, junk_file_cleaner):
    result = junk_file_cleaner.scan_preferences_for_deleted_apps(
        ["/prefs"], ["*.plist"], ["excluded_app"]
    )
    assert sorted(result) == sorted(["/prefs/file1.plist"])


# Test for 'include_apple_app'
@patch.object(
    util,
    "include_apple",
    return_value=["/apple/app1.plist", "/apple/excluded_app.plist"],
)
def test_include_apple_app(mock_include_apple, junk_file_cleaner):
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = False
    result = junk_file_cleaner.include_apple_app()
    assert sorted(result) == sorted(["/apple/app1.plist", "/apple/excluded_app.plist"])


@patch.object(JunkFileCleaner, "scan_temp_files", return_value=["/temp/file1.tmp"])
@patch.object(JunkFileCleaner, "scan_cache", return_value=["/cache/file1.cache"])
@patch.object(
    JunkFileCleaner,
    "scan_preferences_for_deleted_apps",
    return_value=["/prefs/file1.plist"],
)
def test_scan_junk_files(
    mock_scan_temp, mock_scan_cache, mock_scan_pref, junk_file_cleaner
):
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = False
    result = junk_file_cleaner.scan_junk_files()
    expected_result = ["/temp/file1.tmp", "/cache/file1.cache", "/prefs/file1.plist"]
    assert sorted(result) == sorted(expected_result)
