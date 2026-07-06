return{
    { 
        "catppuccin/nvim", 
        name = "catppuccin", 
        priority = 1000,
        config = function()
            vim.cmd.colorscheme("catppuccin")
        end,
    },
    {
        "folke/tokyonight.nvim",
        priority = 1000
    },
    {
        "scottmckendry/cyberdream.nvim",
        priority = 1000,
    },
    {
        "rebelot/kanagawa.nvim",
        priority = 1000,
    },
    {
        "navarasu/onedark.nvim",
        priority = 1000,
    },
    {
        "nvim-lualine/lualine.nvim",
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },

        config = function()
            require("lualine").setup()
        end,
    },
    {
        "akinsho/bufferline.nvim",
        version = "*",
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },

        config = function()
            require("bufferline").setup({})
        end,
    },
    {
        "nvim-neo-tree/neo-tree.nvim",
        branch = "v3.x",
        dependencies = {
        "nvim-lua/plenary.nvim",
        "MunifTanjim/nui.nvim",
        "nvim-tree/nvim-web-devicons", -- optional, but recommended
        },
        lazy = false, -- neo-tree will lazily load itself
        config = function ()
            require("neo-tree").setup({})

            vim.api.nvim_create_autocmd("VimEnter", {
                callback = function()
                require("neo-tree.command").execute({ toggle = false })
                end,
            })
        end
    },
    {
        "folke/which-key.nvim",
        event = "VeryLazy",
        init = function()
            vim.o.timeout = true
            vim.o.timeoutlen = 300
        end,
        opts = {
        }
    },
    {
        "lukas-reineke/indent-blankline.nvim",
        main = "ibl", -- Required for v3 to properly route to the new entry point
        opts = {},
    }
}
