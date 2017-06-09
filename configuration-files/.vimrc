" Editing
set tabstop=4                  " number of visual spaces per TAB
set softtabstop=4              " number of spaces in tab when editing
set expandtab                  " tabs are spaces
set backspace=indent,eol,start " normal backspacing
set autoindent

" Visual
syntax enable                  " syntax highlighting
set showmatch                  " highlight matching [{()}]
set hlsearch                   " highlight matches of search results
set incsearch                  " highlight matches of search results in realtime
set nowrap                     " don't wrap text around

" Other
set mouse-=a                   " disable switching to Visual mode on mouse highlighting

" Remember last position when reopening file
if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
endif
