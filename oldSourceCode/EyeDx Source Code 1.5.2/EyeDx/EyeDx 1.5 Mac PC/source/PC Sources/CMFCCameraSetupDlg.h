#pragma once#define WINDOWS#include "main.h"class CMFCCameraSetupDlg : public CDialog{public:	CMFCCameraSetupDlg(CMainWindow *pParentWnd, CEyeDxBooleanType autoStart) :		CDialog(IDD_PREPARE_CAMERA_DIALOG, (CWnd *)pParentWnd) 		{ 			m_Parent = pParentWnd;			m_AutoStart = autoStart;		}			virtual CEyeDxBooleanType	OnInitDialog();	afx_msg CEyeDxBooleanType	OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*);	virtual void	OnManualPressed();	protected:		DECLARE_MESSAGE_MAP()private:	CMainWindow			*m_Parent;	CEyeDxBooleanType	m_AutoStart;		CBitmap				m_hCameraSetupBitmap;};