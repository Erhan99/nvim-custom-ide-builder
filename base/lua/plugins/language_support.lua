local function get_language_config()
  local ok, languages = pcall(require, "config.languages")

  if ok and type(languages) == "table" then
    return languages
  end

  return {
    lsp_servers = {},
    formatters_by_ft = {},
  }
end

return {
  {
    "williamboman/mason.nvim",
    config = function()
      require("mason").setup()
    end,
  },

  {
    "williamboman/mason-lspconfig.nvim",
    dependencies = {
      "williamboman/mason.nvim",
      "neovim/nvim-lspconfig",
    },
    config = function()
      local languages = get_language_config()

      require("mason-lspconfig").setup({
        ensure_installed = languages.lsp_servers or {},
      })
    end,
  },

  {
    "neovim/nvim-lspconfig",
    config = function()
      local languages = get_language_config()

      for _, server in ipairs(languages.lsp_servers or {}) do
        -- Use the built-in LSP config API instead of the deprecated framework.
        vim.lsp.config(server, {})
        vim.lsp.enable(server)
      end
    end,
  },

  {
    "stevearc/conform.nvim",
    opts = function(_, opts)
      opts = opts or {}
      local languages = get_language_config()
      opts.formatters_by_ft = vim.tbl_deep_extend(
        "force",
        opts.formatters_by_ft or {},
        languages.formatters_by_ft or {}
      )
    end,
  },
}
