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


@patch.object(
    JunkFileCleaner,
    "find_files_by_pattern",
    return_value=["/temp/file1.tmp", "/temp/excluded_app/file2.tmp"],
)
def test_scan_files(mock_find_files, junk_file_cleaner):
    result = junk_file_cleaner.scan_files(["/temp"], ["*.tmp"], ["excluded_app"])
    assert sorted(result) == sorted(["/temp/file1.tmp"])


@patch.object(
    util,
    "include_apple",
    return_value=["/apple/app1.plist", "/apple/excluded_app.plist"],
)
def test_include_apple_app(mock_include_apple, junk_file_cleaner):
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = False
    result = junk_file_cleaner.include_apple_app()
    assert sorted(result) == sorted(["/apple/app1.plist", "/apple/excluded_app.plist"])


@patch.object(JunkFileCleaner, "scan_files")
@patch.object(JunkFileCleaner, "include_apple_app")
def test_scan_junk_files(mock_include_apple_app, mock_scan_files, junk_file_cleaner):
    # Mock dependencies
    junk_file_cleaner.ui.clear_tree = MagicMock()
    junk_file_cleaner.ui.show_question = MagicMock(return_value=True)
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = True
    mock_include_apple_app.return_value = ["app1", "app2"]
    mock_scan_files.side_effect = [
        ["temp_file1", "temp_file2"],  # Temporary files
        ["cache_file1", "cache_file2"],  # Cache files
        ["pref_file1"],  # Preference files
    ]
    junk_file_cleaner.add_file_to_ui = MagicMock()

    # Call the method
    result = junk_file_cleaner.scan_junk_files()

    # Assertions
    junk_file_cleaner.ui.clear_tree.assert_called_once()
    junk_file_cleaner.ui.show_question.assert_called_once_with(
        "Are you sure to include Apple applications?"
    )
    mock_include_apple_app.assert_called_once()
    mock_scan_files.assert_any_call(util.temp_paths(), ["*"], ["app1", "app2"])
    mock_scan_files.assert_any_call(util.cache_paths(), ["*"], ["app1", "app2"])
    mock_scan_files.assert_any_call(
        util.preference_paths(), ["*.plist"], ["app1", "app2"]
    )
    junk_file_cleaner.add_file_to_ui.assert_any_call(
        ["temp_file1", "temp_file2"], "Temporary Files"
    )
    junk_file_cleaner.add_file_to_ui.assert_any_call(
        ["cache_file1", "cache_file2"], "Cache Files"
    )
    junk_file_cleaner.add_file_to_ui.assert_any_call(["pref_file1"], "Preference Files")

    # Validate the final result
    expected_result = [
        "temp_file1",
        "temp_file2",
        "cache_file1",
        "cache_file2",
        "pref_file1",
    ]
    assert result == expected_result


@patch("os.path.basename", side_effect=lambda x: x.split("/")[-1])
@patch("os.access", side_effect=lambda x, _: x.startswith("/writable"))
def test_add_file_to_ui(mock_access, mock_basename, junk_file_cleaner):
    # Arrange: Mock files and category
    files = ["/writable/file1.txt", "/readonly/file2.log"]
    category = "Test Category"

    # Act: Call the method
    junk_file_cleaner.add_file_to_ui(files, category)

    # Assert: Ensure `ui.add_tree_item` was called with the correct parameters
    junk_file_cleaner.ui.add_tree_item.assert_any_call(
        "file1.txt", "/writable/file1.txt", category, True
    )
    junk_file_cleaner.ui.add_tree_item.assert_any_call(
        "file2.log", "/readonly/file2.log", category, False
    )

    # Verify the number of calls
    assert junk_file_cleaner.ui.add_tree_item.call_count == 2
