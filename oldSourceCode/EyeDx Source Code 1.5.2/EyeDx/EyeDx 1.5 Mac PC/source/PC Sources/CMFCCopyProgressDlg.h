/////////////////////////////////////////////////////////////////////////////// Copyright (C) 1998 by Jorge Lodos// All rights reserved//// Distribute and use freely, except:// 1. Don't alter or remove this notice.// 2. Mark the changes you made//// Send bug reports, bug fixes, enhancements, requests, etc. to://    lodos@cigb.edu.cu/////////////////////////////////////////////////////////////////////////////#if !defined(AFX_PREVIEWFILEDLG_H__1D054314_0872_11D2_8A46_0000E81D3D27__INCLUDED_)#define AFX_PREVIEWFILEDLG_H__1D054314_0872_11D2_8A46_0000E81D3D27__INCLUDED_#if _MSC_VER >= 1000#pragma once#endif // _MSC_VER >= 1000// PreviewFileDlg.h : header file///////////////////////////////////////////////////////////////////////////////// CMFCCopyProgressDlg dialogclass CMFCCopyProgressDlg : public CDialog{	DECLARE_DYNAMIC(CMFCCopyProgressDlg)	public:	virtual BOOL 	OnInitDialog();	afx_msg BOOL	OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*);		CMFCCopyProgressDlg(BOOL *CancelPressed);	void			SetActionText(CString str);	void			SetStepText(CString str);	// Attributesprotected:	virtual	void	OnCancel();	CStatic			*m_ActionCtrl;	CStatic			*m_StepCtrl;		DECLARE_MESSAGE_MAP()private:	BOOL			*CancelPressedPtr;};//{{AFX_INSERT_LOCATION}}// Microsoft Developer Studio will insert additional declarations immediately before the previous line.#endif // !defined(AFX_PREVIEWFILEDLG_H__1D054314_0872_11D2_8A46_0000E81D3D27__INCLUDED_)