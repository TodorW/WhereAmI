# Bash completion for whereami.
#
# Usage:
#   source completions/whereami.bash
# or, to load it in every new shell, add that line to your ~/.bashrc.

_whereami_completions() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD - 1]}"

    opts="--version --username --email --category --only-found --workers --timeout \
--host-concurrency --diff --check-breach --output --format --no-color --quiet \
--config --list-categories --help"

    case "$prev" in
        --format)
            COMPREPLY=($(compgen -W "json csv" -- "$cur"))
            return 0
            ;;
        --output|--diff|--config)
            COMPREPLY=($(compgen -f -- "$cur"))
            return 0
            ;;
    esac

    COMPREPLY=($(compgen -W "$opts" -- "$cur"))
}

complete -F _whereami_completions whereami
complete -F _whereami_completions whereami.py
