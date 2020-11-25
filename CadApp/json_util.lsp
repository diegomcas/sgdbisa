;;-----------------------------------------------------------------------------------------
;;str_replace function.
;;Replace all aparisions of "patt" by "repl_to"
;;
;;Params:
;;  -str: The original string
;;  -patt: The pattern which will be replaced
;;  -repl_to: The string which will replace the pattern
;;
;;Original Code by: diegomcas, 2020/03/25
;-----------------------------------------------------------------------------------------
(defun str_replace(str patt repl_to / pos inc)

  (if (not str) (setq str ""))
  (if (and (not patt) (< (strlen patt) 1)) (setq patt " "))
  (if (and (not repl_to) (< (strlen repl_to) 1)) (setq repl_to " "))

  (setq pos (vl-string-search patt str))
  (setq inc (1+ (- (strlen repl_to) (strlen patt))))
  (while pos
    (setq str (vl-string-subst repl_to patt str pos))
    (setq pos (vl-string-search patt str (+ pos inc)))
  )
  str
)

;;-----------------------------------------------------------------------------------------
;;json_parser function (To be executed by json_to_list)
;;Make a list of list with all data of the json string.
;;One list for each of:
;;  -pairs name:value
;;  -arrays
;;  -objets
;;
;;Params:
;;  -lst_json: The list prepared by (json_to_list) function
;;  -state:  for the use of the States Machine
;;
;;Original Code by: diegomcas, 2020/03/25
;;-----------------------------------------------------------------------------------------
(defun json_parser(lst_json state / lst str_name res)

  (setq lst '())
  (setq lst_pair '())

  (if (not state)
    (setq state 'Obj)
  )

  (foreach res lst_json
    (cond
      ((and (eq state 'Obj) (or (eq res 'null) (eq res 'false) (eq res 'true)))
        (setq lst (append lst (list res)))
      )
      ((and (eq state 'Obj_Value) (or (eq res 'null) (eq res 'false) (eq res 'true) (eq (type res) 'STR) (eq (type res) 'INT) (eq (type res) 'REAL)))
        (if (eq 'STR (type res))
          (progn
            (setq res (str_replace res " ," "," ))
            ; (setq res (utf_to_ansi res))
          )
        )
        
        ; (princ "name: ") (princ str_name) (princ " - ")
        ; (princ "value: ") (princ res) (princ "\n")
        
        (setq lst_pair (list str_name res))
        (setq lst (append lst (list lst_pair)))
        (setq str_name nil)
      )
      ((and (eq state 'Obj_Value) (eq res ',))
        (setq state 'Obj)
      )
      ((and (eq state 'Obj) (eq (type res) 'STR))
        (setq str_name res)
        (setq state 'Obj_Name)
      )
      ((and (eq state 'Obj) (eq (type res) 'LIST))
        (setq lst_temp (json_parser res state))
        (setq lst_pair (append str_name lst_temp))
        (setq lst (append lst (list lst_pair)))
        ;(setq lst (append lst lst_pair))
      )
      ((and (eq state 'Obj_Value) (eq (type res) 'LIST))
        (setq lst_temp (json_parser res 'Obj))
        (if str_name
          ;(setq lst_pair (list str_name (list lst_temp)))
          (setq lst_pair (list str_name lst_temp))
          (setq lst_pair lst_temp)
        )
        
        (setq lst (append lst (list lst_pair)))
      )
      ((and (eq state 'Obj_Name) (eq res ':))
        (setq state 'Obj_Value)
      )
    )
  )
  lst
)

;;-----------------------------------------------------------------------------------------
;;json_to_list function
;;Make a list of list with all data of the json string.
;;One list for each of:
;;  -pairs name:value
;;  -arrays
;;  -objets
;;
;;Params:
;;  -json: The json string
;;
;;Original Code by: diegomcas, 2020/03/25
;;-----------------------------------------------------------------------------------------
(defun json_to_list(json / strtransf stread)
  (if (not (eq 'STR (type json)))
    (setq json "{}")
  )

  ;Lists of lists for registers/arrays/objects of the json
  (setq strtransf (vl-string-translate "{}[]" "()()" json))
  ;add spaces before "," / Repairing bad read of numbers
  (setq strtransf (str_replace strtransf "," " ,"))
  (setq strtransf (str_replace strtransf ":" " : "))

  (setq stread (read strtransf))
  ;(princ "json -> ")(princ json) (princ "\n")
  ;(princ "stread -> ")(princ stread) (princ "\n")

  (json_parser stread nil)
)

;;-----------------------------------------------------------------------------------------
;;list_to_json function
;;Make a json string with all data of the json list.
;;
;;Not complete testing!!! Testing for use it!!!
;;Params:
;;  -json: The json string
;;
;;Autolisp don't have Arrays, so it is impossible to rebuild a json that contains them.
;;
;;If you run (setq lst_json (json_to_list "{your_json}")) and then run (json_to_list lst_json)
;;you probably lose data (type of data)
;;
;;Original Code by: diegomcas, 2020/03/25
;;-----------------------------------------------------------------------------------------
(defun list_to_json(lst / lst_element reading json)

  (defun is_object(lst / res)
    (if (eq 'STR (type (car lst)))
      (setq res T)
      (setq res nil)
    )
    res
  )

  (defun read_list(lst json / )
    
    (setq reading 'Obj_or_Arr)
    
    (foreach lst_element lst
      (if (eq 'LIST (type lst_element))
        (progn
          (if (is_object lst_element)
            (progn
              (setq json (read_list lst_element json))
            )
            (progn
              (setq json (strcat json "{"))
              (setq json (read_list lst_element json))
              (setq json (strcat json "}"))
            )
          )
        )
        (progn ;not is list / is name or value
          (cond
            ((not (eq reading 'Value))
              (setq json (strcat json "\"" lst_element "\"" ":"))
              (setq reading 'Value)
            )
            ((eq reading 'Value)
              (cond
                ((eq 'STR (type lst_element))
                  (setq json (strcat json "\"" lst_element "\"" ","))
                )
                ((eq 'REAL (type lst_element))
                  (setq json (strcat json (rtos lst_element 2 2) ","))
                )
                ((eq 'INT (type lst_element))
                  (setq json (strcat json (itoa lst_element) ","))
                )
                ((eq 'NULL lst_element)
                  (setq json (strcat json "null" ","))
                )
                ((eq 'FALSE lst_element)
                  (setq json (strcat json "false" ","))
                )
                ((eq 'TRUE lst_element)
                  (setq json (strcat json "true" ","))
                )
              )
            )
          )
        )
      )
    )
    json
  )
  
  (setq json (read_list lst "{"))
  (setq json (strcat json "}"))
  
  ;Clean the string
  (setq json (str_replace json ",}" "}"))
)

(setq lst_json (json_to_list "{\"name0\": {\"name\": \"value\", \"name1\": \"value1\"}, \"name1\": {[\"arr1\", \"arr2\"]}}"))
