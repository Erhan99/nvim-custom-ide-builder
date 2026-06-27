return {
    {
        "nvim-treesitter/nvim-treesitter",
        build = ":TSUpdate",

        opts = {
        ensure_installed = {
            "lua",
            "python",
            "vim",
            "vimdoc",
        },

        highlight = {
            enable = true,
        },

        indent = {
            enable = true,
        },
        },
  },
    { "echasnovski/mini.pairs", enabled = false },
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    opts = {
      check_ts = true, -- Use Tree-sitter to check for context pairs
      disable_filetype = { "TelescopePrompt", "spectre_panel" },
      disable_in_macro = true, -- Stop pairing while recording macros
    },
  },
}