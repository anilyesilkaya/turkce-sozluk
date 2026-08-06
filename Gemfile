source "https://rubygems.org"

gem "jekyll", "~> 4.4.1"

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.9"
  gem "jekyll-sitemap", "~> 1.4"
end

# Required for local Jekyll development on native Windows.
platforms :mingw, :x64_mingw, :mswin do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Improves automatic file watching on native Windows.
gem "wdm", "~> 0.2.0", install_if: Gem.win_platform?