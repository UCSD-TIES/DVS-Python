#pragma once#define WINDOWS#include "main.h"class CMFCStartupSessionDlg : public CDialog{public:	CMFCStartupSessionDlg(CMainWindow *pParentWnd, CEyeDxLongStringType *pSessionName) :		CDialog(IDD_STARTUP_SESSION_DIALOG, (CWnd *)pParentWnd) 		{ 			m_Parent = pParentWnd;			m_SessionName = pSessionName;		}			virtual CEyeDxBooleanType	OnInitDialog();	afx_msg CEyeDxBooleanType	OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*);	protected:		DECLARE_MESSAGE_MAP()private:	CMainWindow					*m_Parent;	CStatic						*m_ctlSessionCaption;	CEyeDxLongStringType		*m_SessionName;};