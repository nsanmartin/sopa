#!/bin/sh
":"; exec emacs --quick --script "$0" "$@" # -*-emacs-lisp-*-


;; Una mala forma de procesar los command-line args...:
(let ((n (if (string= "-n" (car argv))	(string-to-number (cadr argv)) 4))
      (file-name (last argv)))
  (princ
   (with-temp-buffer
     (insert-file-contents (car file-name))
     (keep-lines "^[a-zA-z]+$")
     (flush-lines (concat "^.\\{0," (number-to-string n) "\\}$"))
     (upcase-region (point-min) (point-max))
     (buffer-string))))

(kill-emacs 0)
