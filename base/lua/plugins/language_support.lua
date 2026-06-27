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
            require("mason-lspconfig").setup()
        end,
    },

    {
        "neovim/nvim-lspconfig",
    },

    {
        "stevearc/conform.nvim",
        opts = {},
    },
}