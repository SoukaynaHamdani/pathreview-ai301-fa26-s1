"""Tests for GitHubTool metadata fetching."""

from agent.tools.github_tool import GitHubTool


def test_github_tool_metadata_has_file_structure(mocker):
    """Test that GitHubTool metadata includes file_structure."""
    tool = GitHubTool()

    # Mock the internal API calls to avoid real network hits in tests
    mocker.patch.object(tool, "_has_readme", return_value=True)
    mocker.patch.object(
        tool, "_fetch_file_structure", return_value=["tests", ".github", "README.md"]
    )

    # Mock httpx.get for main repo metadata
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "test-repo",
        "description": "A test repository",
        "language": "Python",
        "stargazers_count": 10,
        "forks_count": 2,
        "open_issues_count": 0,
        "pushed_at": "2026-01-01T00:00:00Z",
    }
    mocker.patch("httpx.get", return_value=mock_response)

    result = tool.execute({"github_username": "testuser", "repo_name": "testrepo"})

    assert result.success is True
    assert "file_structure" in result.data
    assert result.data["file_structure"] == ["tests", ".github", "README.md"]
