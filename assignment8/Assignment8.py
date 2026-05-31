# Task 1: Review robots.txt to Ensure Policy Compliance
# Checked: https://durhamcountylibrary.org/robots.txt
# Policy Assessment: 
#   - User-agent: * applies to this custom Selenium script.
#   - Path '/wp-admin/' is forbidden.
#   - Public library content data collection is permitted.
#   - Conclusion: The target scraping steps do not breach the site policy.

# Task 2: Understanding HTML and the DOM for the Durham Library Site
# Documented Class Values and HTML Structures:
# 
# 1. Single Entry Container:
#    - HTML Tag: <li>
#    - Class Value: row cp-search-result-item
#
# 2. Title Element:
#    - HTML Tag: <span>
#    - Class Value: cp-title
#
# 3. Author Element:
#    - HTML Tag: <a> (Anchor link)
#    - Class Value: author-link
#    - Strategy for Multiple Authors: Use find_elements() to capture all instances.
#
# 4. Format and Year Container:
#    - Parent HTML Tag: <div>
#    - Parent Class Value: manifestation-details
#    - Specific Year Tag/Class: span.cp-published-year
# 