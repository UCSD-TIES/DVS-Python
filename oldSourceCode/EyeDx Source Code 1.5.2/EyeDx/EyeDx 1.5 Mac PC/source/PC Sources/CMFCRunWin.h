// CMFCRunWin.h#pragma once// This is the base class for the Run windows. It handles the common// operations between the Camera and Disk-based Run Windows. Several// member functions are pure virtual, and the derived classes must override them.// Forward declarationclass CMainWindow;class CMFCRunWin : public CWnd{	public:			CMFCRunWin(CRect *posRect, CMainWindow *myParent, CEyeDxBooleanType *DirectorySet, char *DefaultImagesDir);			protected:			void					Init();			void 					PostNcDestroy();				virtual afx_msg	void	OnSetFocus(CWnd *);		virtual afx_msg int		OnCreate(LPCREATESTRUCT);				virtual afx_msg CEyeDxBooleanType	OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*);				virtual afx_msg	void	OnClose();		virtual afx_msg	void	OnSelectUpButtonClicked();		virtual afx_msg	void	OnSelectSideButtonClicked();		virtual afx_msg	void	OnAnimateCheckboxClicked();				virtual afx_msg	int		OnOkButtonClicked();		virtual afx_msg	void	OnCancelButtonClicked();				DECLARE_MESSAGE_MAP()					CMainWindow			*m_Parent;				CEyeDxBooleanType	*m_DirectorySetPtr;				char				*m_DefaultImagesDir;				int					m_cxChar;		int					m_cyChar;				UINT				m_MessageToSend;			CStatic				m_ctlUpProgressCaption;		CStatic				m_ctlSideProgressCaption;		CProgressCtrl		m_ctlUpProgressBar;		CProgressCtrl		m_ctlSideProgressBar;				CEyeDxDibStatic		m_ctlUpView;		CEyeDxDibStatic		m_ctlSideView;		CStatic				m_ctlUpQualityBitmap;		CStatic				m_ctlSideQualityBitmap;		CStatic				m_ctlSideTopOfHeadBitmap;		CStatic				m_ctlUpCaption;		CStatic				m_ctlSideCaption;		CButton				m_ctlUpSelectButton;		CButton				m_ctlSideSelectButton;		CButton				m_ctlAnimateCheckbox;				CStatic				m_ctlNameCaption;		CEdit				m_ctlNameEditField;		CStatic				m_ctlNameDisplayCaption;				CButton				m_ctlCancelButton;		CButton				m_ctlOkButton;				CStatic				m_ctlLicenseCaption;		CStatic				m_ctlSessionCaption;				CBitmapButton		m_ctlUpZoomButton;		CBitmapButton		m_ctlSideZoomButton;		CEyeDxBooleanType	m_UpSelected;		CEyeDxBooleanType	m_SideSelected;				CEyeDxBooleanType	m_UpDownloaded;		CEyeDxBooleanType	m_SideDownloaded;				DCPictInfo 			m_UpGenericPictInfo;		DCPictInfo 			m_SideGenericPictInfo;		DC120PictInfo		m_UpPictInfo;		DC120PictInfo		m_SidePictInfo;				CEyeDxBooleanType	m_UpPictInfoValid;		CEyeDxBooleanType	m_SidePictInfoValid;		CFont				m_ctlFont;				CBitmap				m_hBadBitmap;		CBitmap				m_hCautionBitmap;		CBitmap				m_hGoodBitmap;		CBitmap				m_hTopOfHeadSidewaysBitmap;		AnalysisResults	 	*m_Results;				CEyeDxVariableList	*m_VariableList;				int					m_PromptStyle;};