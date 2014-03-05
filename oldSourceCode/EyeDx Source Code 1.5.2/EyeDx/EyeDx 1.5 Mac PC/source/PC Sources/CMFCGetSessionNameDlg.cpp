// main.cp#include "main.h"BEGIN_MESSAGE_MAP( CMFCGetSessionNameDlg, CDialog )ON_NOTIFY_EX(TTN_NEEDTEXT, 0, OnToolTipText)END_MESSAGE_MAP()CEyeDxBooleanType CMFCGetSessionNameDlg::OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*){	TOOLTIPTEXT *pTTT = (TOOLTIPTEXT *) pNMHDR;	if (!(pTTT->uFlags & TTF_IDISHWND))	// the ID must be a handle to a window		return FALSE;			UINT uID = pNMHDR->idFrom;	uID = ::GetDlgCtrlID((HWND)uID);			CString strTipText;		// Attempt to load a ToolTip string that corresponds to the control's ID		if(!strTipText.LoadString(uID))		return FALSE;		// Stuff text into the ToolTip, 80 characters maximum		strncpy(pTTT->lpszText, strTipText, 80);	return TRUE;}CEyeDxBooleanType CMFCGetSessionNameDlg::OnInitDialog(){	CDialog::OnInitDialog();	CenterWindow();			EnableToolTips(TRUE);	m_ctlNameField = (CEdit*) (GetDlgItem(IDC_SESSION_NAME_EDIT_FIELD));		m_ctlNameLengthCaption = (CStatic*) (GetDlgItem(IDC_SESSION_NAME_LENGTH_CAPTION));		CString theSessionPrompt;	theSessionPrompt.Format("Please enter up to %d characters for the session name:", kMaxSessionNameLength);	m_ctlNameLengthCaption->SetWindowText(theSessionPrompt);		return TRUE;}void CMFCGetSessionNameDlg::OnOK(){	// Get the entered session name and see if it is valid.	// If it is, we return true. If not, the user is prompted and we	// continue looping.	CString theSessionNameString;		m_ctlNameField->GetWindowText(theSessionNameString);		// Note that this routine also sets the global session_filename variable	// if the entered value is ok.		if (CheckSessionValidity(this, &theSessionNameString))	{		*m_NewSessionName = theSessionNameString;		CDialog::OnOK();	}}