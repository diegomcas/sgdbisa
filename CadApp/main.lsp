(vl-load-com)
(load "settings.lsp")
(load "api_call.lsp")
(load "json_util.lsp")
(command "OPENDCL")

;-------------------------------------------------------------------------------------------------
;Variables Globales
;-------------------------------------------------------------------------------------------------
(setq GLOBAL_TOKEN nil)
(setq GLOBAL_USERNAME nil)
(setq GLOBAL_CURRENT_DOC nil)
(setq GLOBAL_CURRENT_DOC_NAME nil)
;-------------------------------------------------------------------------------------------------
;FIN Variables Globales
;-------------------------------------------------------------------------------------------------

(if (not (eq 'EXRXSUBR (type dcl_Project_Load)))
  (progn
    (princ "No se ha instalado OPENDCL.")
    (exit)
  )
)

(if (not (dcl_Project_Load "documents" T))
  (progn
    (princ "Error al cargar el projecto OPENDCL: 'documents'")
    (exit)
  )
)

(defun c:login( / login_return)
  (setq login_return (dcl_Form_Show documents_Login))
  (if (not (or (eq login_return 100) (eq login_return 2)))
    (dcl-MessageBox "Se produjeron errores al iniciar sesión en el servidor." "Login Incorrecto" 2 2 False)
  )
  (princ)
)

(defun c:sel_doc( / response_find)
  ;selecciono documento
  (setq response_find (dcl_Form_Show documents/Find_Document))
  
  (if (eq response_find 200)
      (dcl_Form_Show documents/Check_Documento)
  )
  (princ)
)

(defun c:check_doc( / )
  (dcl_Form_Show documents/Check_Documento)
  (princ)
)

(defun c:close_session( / )
  (setq GLOBAL_TOKEN nil)
  (setq GLOBAL_USERNAME nil)
  (princ)
)

(defun c:view_session( / )
  (princ "TOKEN: ") (princ GLOBAL_TOKEN) (princ "\n")
  (princ "USERNAME: ") (princ GLOBAL_USERNAME) (princ "\n")
  (princ)
)

;-------------------------------------------------------------------------------------------------
;Eventos del formulario Login
;-------------------------------------------------------------------------------------------------
(defun c:documents/Login#OnCancelarCerrar (is_esc /)
  ;; intIsESC = 1 when ESC key was pressed, the closing button in the titlebar was clicked
  (eval (/= is_esc 1))
)

(defun c:documents/Login#OnInicializar (/)
  (dcl-Control-SetText documents/Login/password "")
  (princ)
)

(defun c:documents/Login/send_login#OnAccionado ( / url_token response_token username password)
  (dcl-Control-SetCaption documents/Login/tag_status "")
  
  (setq username (dcl-Control-GetText documents/Login/username))
  (setq password (dcl-Control-GetText documents/Login/password))
  
  ;Verifico que se ingresaron usuario y contraseña
  (if username
    (if (eq username "")
      (dcl-Control-SetCaption documents/Login/tag_status "Debe ingresar Nombre de usuario")
    )
    (dcl-Control-SetCaption documents/Login/tag_status "Debe ingresar Nombre de usuario")
  )
      
  (if password
    (if (eq password "")
      (if username
        (if (eq username "")
          (dcl-Control-SetCaption documents/Login/tag_status "Debe ingresar Nombre de Usuario y Contraseña")
          (dcl-Control-SetCaption documents/Login/tag_status "Debe ingresar Contraseña")
        )
      )
    )
  )
  
  ;(princ "username: ") (princ username) (princ "\n")
  ;(princ "password: ") (princ password) (princ "\n")

  (if (and username password)
    (if (and (not (eq username "")) (not (eq password "")))
      (progn
        ;Conectar con credenciales del form al API
        (setq url_token (strcat GLOBAL_URL "api-token-auth/"))
        
        (setq response_token (get_DRF_token url_token username password))
        
        ;(princ response_token)(princ "\n")
        
        ;Evaluar Response
        (setq token (cadr response_token))
        (setq response_token (car response_token))
        (if (not token) ;no tengo token
          (progn
            ;(princ (cdr (assoc 'ErrorValue response_token))) (princ "\n")
            (if (cdr (assoc 'ErrorValue response_token))
              (progn
                (dcl-Control-SetCaption documents/Login/tag_status
                  (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_token)))
                )
              )
              (progn
                (dcl-Control-SetCaption documents/Login/tag_status
                  (strcat "Status: " (itoa (cdr (assoc 'Status response_token))) " - "
                          (cdr (assoc 'StatusText response_token)) "\n"
                          "Error: " (cdr (assoc 'ResponseAnsiText response_token))
                  )
                )
              )
            )
          )
          (progn
            ;Cierro Form
            (setq GLOBAL_TOKEN token)
            (setq GLOBAL_USERNAME username)
            (dcl-Form-Close documents/Login 100)
          )
        )
      )
    )
  )
  (princ)
)

;-------------------------------------------------------------------------------------------------
;Eventos del formulario Buscar Documentos
;-------------------------------------------------------------------------------------------------
;-------------------------------------------------------------------------------------------------
; *OnCancelClose* Eventos del formulario Buscar Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Find_Document#OnCancelarCerrar (is_esc /)
  (eval (/= is_esc 1))
)

;-------------------------------------------------------------------------------------------------
; *OnInicializar* Eventos del formulario Buscar Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Find_Document#OnInicializar ( / lst_possible_names lyt_name)
  ;Limpia los controles del formulario
  (dcl-Grid-Clear documents/Find_Document/tbl_documents)
  (dcl-Control-SetCaption documents/Find_Document/tag_status "")
  (dcl-ComboBox-Clear documents/Find_Document/document_name)
  (if GLOBAL_TOKEN
    (progn
      ;Armo lista con nombre posible del documento
      (setq lst_possible_names (list (vl-string-subst "" ".dwg" (getvar "DWGNAME"))))
      
      (vlax-for lyt (vla-get-layouts (vla-get-activedocument (vlax-get-acad-object)))
        (setq lyt_name (vla-get-name lyt))
        (if (not (eq (strcase lyt_name T) "model"))
          (setq lst_possible_names (append lst_possible_names (list lyt_name)))
        )
      )
      
      ;Cargo cuadro combinado con nombre de archivo y nombres de layouts
      (dcl-ComboBox-AddList documents/Find_Document/document_name lst_possible_names)
    )
    (progn
      (dcl-MessageBox "Debe loguearse en el sistema para utilizar esta funcionalidad" "Requiere Loguing" 2 2 False)
      (dcl-Form-Close documents/Find_Document 400)
    )
  )
    
  (princ)
)

;-------------------------------------------------------------------------------------------------
; *OnColumnClick* Eventos del formulario Buscar Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Find_Document/tbl_documents#OnClickEnColumna (column / is_sorted sort)
  (setq is_sorted (dcl-Control-GetSorting documents/Find_Document/tbl_documents))
  (cond
    ((or (eq is_sorted 0) (eq is_sorted 2))
      (setq sort T)
    )
    ((eq is_sorted 1)
      (setq sort nil)
    )
  )
  (if (eq column 0)
    (dcl-Grid-SortNumericCells documents/Find_Document/tbl_documents 0 sort)
    (dcl-Grid-SortTextCells documents/Find_Document/tbl_documents column sort)
  )
  (princ)
)


;-------------------------------------------------------------------------------------------------
; *OnBuscar* Eventos del formulario Buscar Documentos 
;-------------------------------------------------------------------------------------------------
(defun c:documents/Find_Document/send_Buscar#OnAccionado ( 
    / url_docs selection registro valor pk numero tipo tipo_obra revision
      propietario reemplaza_a fecha proyecto titulo)

  ;(princ (dcl-Control-GetCaption documents/Find_Document/tag_status)) (princ "\n")
  (dcl-Grid-Clear documents/Find_Document/tbl_documents)
  (dcl-Control-SetCaption documents/Find_Document/tag_status "")
  
  (setq selection (dcl-ComboBox-GetEBText documents/Find_Document/document_name))
  ;Verifico que se ingresó Numero de Documento
  (if (> (strlen selection) 2)
    (progn
      (setq url_docs (strcat GLOBAL_URL "api-find-docs/" selection))
      (setq response_docs
        (get_from_web url_docs "GET" nil
          (list
            (list "Authorization" (strcat "Token " GLOBAL_TOKEN))
            (list "Content-Type" (strcat "application/json; charset=" GLOBAL_CHARSET))
          )
        )
      )
        
      (princ "response_docs: ") (princ (assoc 'Status response_docs)) (princ "\n")
      
      (if (cdr (assoc 'ErrorValue response_docs))
        (progn
          (dcl-Control-SetForeColor documents/Find_Document/tag_status 1)
          (dcl-Control-SetCaption documents/Find_Document/tag_status
            (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_docs))))
          ;(princ (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_docs))))
        )
        (progn
          (if (equal (cdr (assoc 'Status response_docs)) 200)
            (progn
              (if (equal (cdr (assoc 'Content-Type response_docs)) "application/json")
                (progn
                  (setq lst_res (json_to_list (cdr (assoc 'ResponseAnsiText response_docs))))
                  ;(princ lst_res) (princ "\n")
                  (dcl-Control-SetForeColor documents/Find_Document/tag_status 5)
                  (dcl-Control-SetCaption documents/Find_Document/tag_status
                    (strcat "OK (Status: 200)\n" "Resultado: " (itoa (length lst_res)) " registros."))
                  (foreach registro lst_res
                    (setq pk (itoa (cadr (assoc "pk" registro))))
                    (setq numero (cadr (assoc "numero" registro)))
                    (setq tipo (cadr (assoc "tipo_documento" registro)))
                    (setq tipo_obra (cadr (assoc "tipo_obra" registro)))
                    (setq revision (cadr (assoc "revision" registro)))
                    (setq propietario (cadr (assoc "propietario" registro)))
                    (setq reemplaza_a (cadr (assoc "reemplaza_a" registro)))
                    (setq fecha (cadr (assoc "fecha" registro)))
                    (setq proyecto (cadr (assoc "proyecto" registro)))
                    (setq titulo (cadr (assoc "titulo" registro)))
                    ;(princ tipo_obra) (princ "\n")
                    (dcl-Grid-AddRow documents/Find_Document/tbl_documents
                      pk
                      numero
                      (if (eq tipo 'NULL) " - " tipo)
                      (if (eq tipo_obra 'NULL) " - " tipo_obra)
                      (if (eq revision 'NULL) " - " revision)
                      (if (eq propietario 'NULL) " - " propietario)
                      (if (eq reemplaza_a 'NULL) " - " reemplaza_a)
                      (if (eq fecha 'NULL) " - " fecha)
                      (if (eq proyecto 'NULL) " - " proyecto)
                      (if (eq titulo 'NULL) " - " titulo)
                    )
                  )
                )
                (progn
                  (dcl-Control-SetForeColor documents/Find_Document/tag_status 1)
                  (dcl-Control-SetCaption documents/Find_Document/tag_status
                    (strcat "Response Content-Type not is application/json: "
                    "\nContent-Type: "
                    (cdr (assoc 'Content-Type response_docs))))
                )
              )
            )
            (progn
              (dcl-Control-SetForeColor documents/Find_Document/tag_status 1)
              (dcl-Control-SetCaption documents/Find_Document/tag_status
                (strcat "Status: "
                (itoa (cdr (assoc 'Status response_docs)))
                " - Status Text: "
                (cdr (assoc 'StatusText response_docs))
                "\nResponse Text: "
                (cdr (assoc 'ResponseAnsiText response_docs)))
              )
            )
          )
        )
      )
    )
    (progn
      (dcl-Control-SetForeColor documents/Find_Document/tag_status 1)
      (dcl-Control-SetCaption documents/Find_Document/tag_status
        "Debe ingresar un nombre de documento válido\no una parte de éste mayor a dos caracteres")
    )
  )
  (princ)
)

;-------------------------------------------------------------------------------------------------
; *OnSeleccionar* Eventos del formulario Buscar Documentos (dcl-Grid-GetCurCell documents/Find_Document/tbl_documents)
;-------------------------------------------------------------------------------------------------
(defun c:documents/Find_Document/sel_document#OnAccionado ( / cur_selection)
  (setq cur_selection (car (dcl-Grid-GetCurCell documents/Find_Document/tbl_documents)))
  (if (> cur_selection -1)
    (progn
      (setq GLOBAL_CURRENT_DOC_NAME (cadr (dcl-Grid-GetRowCells documents/Find_Document/tbl_documents cur_selection)))
      (setq GLOBAL_CURRENT_DOC (atoi (car (dcl-Grid-GetRowCells documents/Find_Document/tbl_documents cur_selection))))
      (dcl-Form-Close documents/Find_Document 200)
    )
    (progn
      (dcl-MessageBox "Debe seleccionar un elemento en la tabla." "Selección Vacía" 2 2 False)
    )
  )
  (princ)
  ;(princ GLOBAL_CURRENT_DOC_NAME) (princ "\n") (princ GLOBAL_CURRENT_DOC)
)

;-------------------------------------------------------------------------------------------------
;Eventos del formulario Check Documents
;-------------------------------------------------------------------------------------------------
;-------------------------------------------------------------------------------------------------
; *OnCancelClose* Eventos del formulario Check Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Check_Documento#OnCancelarCerrar (is_esc /)
  (eval (/= is_esc 1))
)

;-------------------------------------------------------------------------------------------------
; *Oninitialize* Eventos del formulario Check Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Check_Documento#OnInicializar ( 
  / response_checks url_checks num_doc propietario checks pk verificado verificado_por
    aplica check_type chkt_nombre chkt_ayuda row_add)
  ;Limpia los controles del formulario
  ;(princ (type documents/Check_Documento/tbl_ckecs))
  (dcl-Grid-Clear documents/Check_Documento/tbl_ckecs)
  (dcl-Control-SetCaption documents/Check_Documento/tag_status "")

  (if GLOBAL_TOKEN
    (progn
      (if GLOBAL_CURRENT_DOC
        (progn
          ;Consultar según valor de GLOBAL_CURRENT_DOC
          (setq url_checks (strcat GLOBAL_URL "api-doc-chequeo/" (itoa GLOBAL_CURRENT_DOC) "/get/"))
          (setq response_checks
            (get_from_web url_checks "GET" nil
              (list
                (list "Authorization" (strcat "Token " GLOBAL_TOKEN))
                (list "Content-Type" (strcat "application/json; charset=" GLOBAL_CHARSET))
              )
            )
          )
          ;Cargar la tabla
          (if (cdr (assoc 'ErrorValue response_checks))
            (progn
              (dcl-Control-SetForeColor documents/Check_Documento/tag_status 1)
              (dcl-Control-SetCaption documents/Check_Documento/tag_status
                (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_checks))))
              ;(princ (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_checks))))
            )
            (progn
              (if (equal (cdr (assoc 'Status response_checks)) 200)
                (progn
                  (if (equal (cdr (assoc 'Content-Type response_checks)) "application/json")
                    (progn
                      (setq lst_res (json_to_list (cdr (assoc 'ResponseAnsiText response_checks))))
                      ;(princ lst_res) (princ "\n")
                      (dcl-Control-SetForeColor documents/Check_Documento/tag_status 5)
                      (dcl-Control-SetCaption documents/Check_Documento/tag_status
                        (strcat "OK (Status: 200)\n" "Resultado: " (itoa (length lst_res)) " registros."))
                      (setq propietario (cadr (assoc "propietario" lst_res)))
                      (setq num_doc (cadr (assoc "numero" lst_res)))
                      (dcl-Control-SetTitleBarText
                        documents/Check_Documento
                        (strcat "Checkear Documento. Nro: " num_doc "; Propietario: " propietario))
                      (setq checks (cadr (assoc "chequeo_documento" lst_res)))
                      ;(princ (dcl-Grid-GetColumnCount documents/Check_Documento/tbl_ckecs)) (princ "\n")
                      (foreach chk checks
                        (setq pk (itoa (cadr (assoc "pk" chk))))
                        (setq aplica (cadr (assoc "aplica" chk)))
                        (setq verificado (cadr (assoc "verificado" chk)))
                        (setq verificado_por (cadr (assoc "verificado_por" chk)))
                        (setq check_type (cadr (assoc "tipo_chequeo" chk)))
                        (setq chkt_nombre (cadr (assoc "nombre" check_type)))
                        (setq chkt_ayuda (cadr (assoc "ayuda" check_type)))
                        
                        ; (princ "pk: ") (princ pk) (princ "\n")
                        ; (princ "verificado: ") (princ verificado) (princ "\n")
                        ; (princ "verificado_por: ") (princ verificado_por) (princ "\n")
                        ; (princ "check_type: ") (princ check_type) (princ "\n")
                        ; (princ "chkt_nombre: ") (princ chkt_nombre) (princ "\n")
                        ; (princ "chkt_ayuda: ") (princ chkt_ayuda) (princ "\n")
                        (setq row_add (dcl-Grid-AddRow documents/Check_Documento/tbl_ckecs
                          pk
                          ""
                          ""
                          (if (eq verificado_por 'NULL) " - " verificado_por)
                          chkt_nombre
                          chkt_ayuda
                        ))
                        ;poniendo el valor al check
                        (dcl-Grid-SetCellCheckState documents/Check_Documento/tbl_ckecs row_add 1 (if (eq aplica 'TRUE) 1 0))
                        (dcl-Grid-SetCellCheckState documents/Check_Documento/tbl_ckecs row_add 2 (if (eq verificado 'TRUE) 1 0))
                      )
                    )
                    (progn
                      (dcl-Control-SetForeColor documents/Check_Documento/tag_status 1)
                      (dcl-Control-SetCaption documents/Check_Documento/tag_status
                        (strcat "Response Content-Type not is application/json: "
                        "\nContent-Type: "
                        (cdr (assoc 'Content-Type response_checks))))
                    )
                  )
                )
                (progn
                  (dcl-Control-SetForeColor documents/Check_Documento/tag_status 1)
                  (dcl-Control-SetCaption documents/Check_Documento/tag_status
                    (strcat "Status: "
                    (cdr (assoc 'Status response_checks))
                    " - Status Text: "
                    (cdr (assoc 'StatusText response_checks))
                    "\nResponse Text: "
                    (cdr (assoc 'ResponseAnsiText response_checks)))
                  )
                )
              )
            )
          )
        )
        (progn
          (dcl-MessageBox "No se ha seleccionado un documento a checkear" "Selccionar documento" 2 2 False)
          (dcl-Form-Close documents/Find_Document 404)
        )
      )
    )
    (progn
      (dcl-MessageBox "Debe loguearse en el sistema para utilizar esta funcionalidad" "Requiere Loguing" 2 2 False)
      (dcl-Form-Close documents/Find_Document 400)
    )
  )
  (princ)
)
;-------------------------------------------------------------------------------------------------
; *OnFinEdicEt* Eventos del formulario Check Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Check_Documento/tbl_ckecs#OnFinEdicEt (Row Column / act_val)
  (if (eq Column 1) ;Aplica
    (progn
      ;Apagando
      (dcl-Grid-SetCellText documents/Check_Documento/tbl_ckecs Row 3 " - ")
      ;Apaga verificado
      (dcl-Grid-SetCellCheckState documents/Check_Documento/tbl_ckecs Row 2 0)
    )
  )
  (if (eq Column 2) ;Verificado
    (progn
      (setq act_val (dcl-Grid-GetCellCheckState documents/Check_Documento/tbl_ckecs Row Column))
      (if (eq act_val 0)
        (progn
          ;Apagando
          (dcl-Grid-SetCellText documents/Check_Documento/tbl_ckecs Row 3 " - ")
        )
        (progn
          ;Encendiendo
          (if (eq (dcl-Grid-GetCellCheckState documents/Check_Documento/tbl_ckecs Row 1) 1)
            (dcl-Grid-SetCellText documents/Check_Documento/tbl_ckecs Row 3 GLOBAL_USERNAME)
            (dcl-Grid-SetCellCheckState documents/Check_Documento/tbl_ckecs Row 2 0)
          )
        )
      )
    )
  )
  (princ)
)

;-------------------------------------------------------------------------------------------------
; *OnSave* Eventos del formulario Check Documentos
;-------------------------------------------------------------------------------------------------
(defun c:documents/Check_Documento/act_save#OnAccionado (
          / count_rows cont chk_pk str_json url_checks chk_by chk_aplied chk_checked)
  ;Si la tabla tiene algo
  (setq count_rows (dcl-Grid-GetRowCount documents/Check_Documento/tbl_ckecs))
  (setq cont 0)
  (setq str_json "[")
  (while (< cont count_rows)
    ;Armo string json PUT
    (setq chk_pk (dcl-Grid-GetCellText documents/Check_Documento/tbl_ckecs cont 0))
    ;(princ "chk_pk= ") (princ chk_pk) (princ "\n")
    (setq chk_aplied 
      (if (eq 0 (dcl-Grid-GetCellCheckState documents/Check_Documento/tbl_ckecs cont 1))
        "false"
        "true"
      )
    )
    (setq chk_checked 
      (if (eq 0 (dcl-Grid-GetCellCheckState documents/Check_Documento/tbl_ckecs cont 2))
        "false"
        "true"
      )
    )
    ;(princ "chk_checked= ") (princ chk_checked) (princ "\n")
    (setq chk_by 
      (if (eq " - " (dcl-Grid-GetCellText documents/Check_Documento/tbl_ckecs cont 3))
        "null"
        (strcat "\"" (dcl-Grid-GetCellText documents/Check_Documento/tbl_ckecs cont 3) "\"")
      )
    )
    ;(princ "chk_by= ") (princ chk_by) (princ "\n")

    (setq str_json (strcat str_json
      "{\"pk\":" chk_pk
      ",\"aplica\":" chk_aplied
      ",\"verificado\":" chk_checked
      ",\"verif_by\":" chk_by "},"))
    (setq cont (1+ cont))
  )
  ;b'[{"id":30,"verificado":false,"verif_by":null},{"id":31,"verificado":true,"verif_by":"diegomcas"},{"id":32,"verificado":false,"verif_by":null}]'
  (setq str_json (vl-string-right-trim "," str_json))
  (setq str_json (strcat str_json "]"))
  
  ;(princ "\n") (princ "str_json= ") (princ str_json) (princ "\n")

  (setq url_checks (strcat GLOBAL_URL "api-doc-chequeo/put/"))
  (setq response_checks
    (get_from_web url_checks "PUT" str_json
      (list
        (list "Authorization" (strcat "Token " GLOBAL_TOKEN))
        (list "Content-Type" (strcat "application/json; charset=" GLOBAL_CHARSET))
      )
    )
  )
  ;Verifica el status
  (if (cdr (assoc 'ErrorValue response_checks))
    (progn
      (dcl-Control-SetForeColor documents/Check_Documento/tag_status 1)
      (dcl-Control-SetCaption documents/Check_Documento/tag_status
        (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_checks))))
      ;(princ (strcat "Server Conection ERROR: " (cdr (assoc 'ErrorValue response_checks))))
    )
    (progn
      (if (equal (cdr (assoc 'Status response_checks)) 200)
        (progn
          (if (equal (cdr (assoc 'Content-Type response_checks)) "application/json")
            (progn
              (setq lst_res (json_to_list (cdr (assoc 'ResponseAnsiText response_checks))))
              ;(princ "\n") (princ "lst_res= ") (princ lst_res) (princ "\n")
              (dcl-Control-SetForeColor documents/Check_Documento/tag_status 5)
              (dcl-Control-SetCaption documents/Check_Documento/tag_status
                (strcat "OK (Status: 200)\n" "Resultado: " (itoa (length lst_res)) " registros actualizados."))
            )
            (progn
              (dcl-Control-SetForeColor documents/Check_Documento/tag_status 1)
              (dcl-Control-SetCaption documents/Check_Documento/tag_status
                (strcat "Response Content-Type not is application/json: "
                "\nContent-Type: "
                (cdr (assoc 'Content-Type response_checks))))
            )
          )
        )
        (progn
          (dcl-Control-SetForeColor documents/Check_Documento/tag_status 1)
          (dcl-Control-SetCaption documents/Check_Documento/tag_status
            (strcat "Status: "
            (itoa (cdr (assoc 'Status response_checks)))
            " - Status Text: "
            (cdr (assoc 'StatusText response_checks))
            "\nResponse Text: "
            (cdr (assoc 'ResponseAnsiText response_checks)))
          )
        )
      )
    )
  )
  (princ)
)




