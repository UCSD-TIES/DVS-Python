#pragma once#define WINDOWS#include "main.h"class CMFCTakePictureDlg : public CDialog{public:	CMFCTakePictureDlg(CMFCRunFromCameraAutoWin *pParentWnd, enum eOrientation pOrientation,											DCPictInfo *pGenericPictInfo,											DC120PictInfo *pPictInfo, 										    CEyeDxDibStatic *pMainWindowView, 										    CStatic *pMainWindowCaption,										    EyeDxNextStepCode theResult) :		CDialog(IDD_PREPARE_PICTURE_DIALOG, (CWnd *)pParentWnd) 		{ 			m_Parent = pParentWnd;			m_Orientation = pOrientation;			m_GenericPictInfo = pGenericPictInfo;			m_PictInfo = pPictInfo;			m_MainWindowView = pMainWindowView;			m_MainWindowCaption = pMainWindowCaption;			m_TheResult = theResult;		}			virtual CEyeDxBooleanType	OnInitDialog();	afx_msg CEyeDxBooleanType	OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*);	virtual CEyeDxBooleanType	PreTranslateMessage(MSG *pMsg);		virtual void	OnOK();	protected:		CMFCRunFromCameraAutoWin *m_Parent;	enum eOrientation 	m_Orientation;	DCPictInfo 			*m_GenericPictInfo;	DC120PictInfo 		*m_PictInfo;	CEyeDxDibStatic 	*m_MainWindowView;	CStatic 			*m_MainWindowCaption;	short				m_TheResult;		HACCEL				m_hAccel;		DECLARE_MESSAGE_MAP()private:	CButton				*m_ctlOkButton;	CButton				*m_ctlCancelButton;	CStatic				*m_ctlTakePictureCaption;	CStatic				*m_ctlBatteryLevelCaption;	CStatic				*m_ctlBatteryLevelBitmap;	CStatic				*m_ctlCameraBitmap;	CBitmap				m_hBatteryOKBitmap;	CBitmap				m_hBatteryWeakBitmap;	CBitmap				m_hBatteryEmptyBitmap;	CBitmap				m_hCameraUpBitmap;	CBitmap				m_hCameraSideBitmap;};