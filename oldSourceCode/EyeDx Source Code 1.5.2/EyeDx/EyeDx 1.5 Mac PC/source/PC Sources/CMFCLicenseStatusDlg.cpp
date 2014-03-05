// main.cp#include <stdio.h>#include <windows.h>#include <wingdi.h>#include <winbase.h>#include <winuser.h>#include <process.h>#include "resource.h"#include "main.h"#include "CMFCLicenseStatusDlg.h"#if defined (WIN32)	#define IS_WIN32	TRUE#else	#define IS_WIN32	FALSE#endifBEGIN_MESSAGE_MAP( CMFCLicenseStatusDlg, CDialog )ON_NOTIFY_EX(TTN_NEEDTEXT, 0, OnToolTipText)END_MESSAGE_MAP()CEyeDxBooleanType CMFCLicenseStatusDlg::OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*){	TOOLTIPTEXT *pTTT = (TOOLTIPTEXT *) pNMHDR;	if (!(pTTT->uFlags & TTF_IDISHWND))	// the ID must be a handle to a window		return FALSE;			UINT uID = pNMHDR->idFrom;	uID = ::GetDlgCtrlID((HWND)uID);			CString strTipText;		// Attempt to load a ToolTip string that corresponds to the control's ID		if(!strTipText.LoadString(uID))		return FALSE;		// Stuff text into the ToolTip, 80 characters maximum		strncpy(pTTT->lpszText, strTipText, 80);	return TRUE;}CEyeDxBooleanType CMFCLicenseStatusDlg::OnInitDialog(){	CDialog::OnInitDialog();	CenterWindow();			m_ctlExpDate = (CStatic *) GetDlgItem(IDC_LICENSE_STATUS_EXPDATE);	m_ctlAnalysisRuns = (CStatic *) GetDlgItem(IDC_LICENSE_STATUS_ANALYSISRUNS);	m_ctlCaption = (CStatic *) GetDlgItem(IDC_LICENSE_STATUS_CAPTION);	EnableToolTips(TRUE);		CString theDateStatusString;	CString theCountStatusString;	CString theDateString;	CString theCountString;		m_Parent->GetLicenseExpDateString(theDateString);	m_Parent->GetLicenseCountString(theCountString);		// By default, set the output strings to the returned values		theDateStatusString = theDateString;	theCountStatusString = theCountString;	switch (m_Status)	{	case LicenseStatusExpiredDate:		theDateStatusString = "Expired on " + theDateString + ".";		theCountStatusString = theCountString + " Analysis Runs Remaining.";		m_ctlCaption->SetWindowText("Request a new license with a new expiration date (and additional runs, if desired). The remaining run count will be added to the amount in the new license.");		break;	case LicenseStatusExpiredCount:		theDateStatusString = "Previous license was valid through " + theDateString + ".";		theCountStatusString = "No Analysis Runs Remaining.";		m_ctlCaption->SetWindowText("Request a new license with additional runs.");		break;	case LicenseStatusExpiredBoth:		theDateStatusString = "Expired on " + theDateString + ".";		theCountStatusString = "No Analysis Runs Remaining.";		m_ctlCaption->SetWindowText("Request a new license with additional runs and a new expiration date.");		break;	case LicenseStatusDateOutOfRange:		theDateStatusString = "Valid through midnight on " + theDateString + ".";		theCountStatusString = theCountString + " Analysis Runs Remaining.";		m_ctlCaption->SetWindowText("The system clock appears to have been reset - license not currently valid.");		break;	default:		theDateStatusString = "Valid through midnight on " + theDateString + ".";		theCountStatusString = theCountString + " Analysis Runs Available.";		m_ctlCaption->SetWindowText("Your license is currently valid.");		break;	}		m_ctlExpDate->SetWindowText(theDateStatusString);		m_ctlAnalysisRuns->SetWindowText(theCountStatusString);		return TRUE;}