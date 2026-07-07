local function get_language_config()
  local ok, languages = pcall(require, "config.languages")

  if ok and type(languages) == "table" then
    return languages
  end

  return {
    treesitter = {},
  }
end

return {
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    opts = function(_, opts)
      opts = opts or {}
      local languages = get_language_config()

      opts.ensure_installed = vim.list_extend(
        { "lua", "vim", "vimdoc" },
        languages.treesitter or {}
      )

      opts.highlight = {
        enable = true,
      }

      opts.indent = {
        enable = true,
      }
    end,
  },
  { "echasnovski/mini.pairs", enabled = false },
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    opts = {
      check_ts = true,
      disable_filetype = { "TelescopePrompt", "spectre_panel" },
      disable_in_macro = true,
    },
  },
}
