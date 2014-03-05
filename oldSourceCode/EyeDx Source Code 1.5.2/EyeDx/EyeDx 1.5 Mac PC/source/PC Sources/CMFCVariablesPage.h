#pragma once#define WINDOWS#include "resource.h"class CMFCVariablesPage : public CPropertyPage{	DECLARE_DYNCREATE(CMFCVariablesPage)public:	CMFCVariablesPage() : CPropertyPage(IDD_VARIABLES_PAGE) {}			virtual CEyeDxBooleanType	OnInitDialog();	afx_msg CEyeDxBooleanType	OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*);	afx_msg void 				OnSize(UINT nType, int cx, int cy);		CEyeDxVariableList	*m_VariableList;		BOOL				m_showHidden;	int					m_PromptingStyle;protected:	void 				DoDataExchange(CDataExchange *pDX);	void				OnOK();	void 				OnNewPressed();	void 				OnEditPressed();	void 				OnDeletePressed();	void 				OnExportPressed();	afx_msg void 		OnListClicked(NMHDR *pnmh, LRESULT *pResult);	afx_msg void		OnListDoubleClicked(NMHDR *pnmh, LRESULT *pResult);	afx_msg void 		OnListColumnPressed(NMHDR *pnmh, LRESULT *pResult);	afx_msg void 		OnGetDispInfo(NMHDR *pnmh, LRESULT *pResult);	void				UpdateVariableList(CEyeDxVariable *reselectVariable);	BOOL 				HandleEditVariable(CEyeDxVariableList *theVariableList,											CEyeDxVariable *theVariable, 											BOOL newVariable, 											BOOL showHidden);		void 				UpdateButtons(CEyeDxVariable *theVariable);	void				EditItem(int theItem);DECLARE_MESSAGE_MAP()private:	CDlgItemResizer		m_Resizer;	CImageList			m_imglLarge;	CImageList			m_imglSmall;		CListCtrl			*m_VariableListBox;	CButton				*m_NewButton;	CButton				*m_EditButton;	CButton				*m_DeleteButton;	CButton				*m_SingleDialogCheckbox;		CEyeDxBooleanType	m_Modified;		int					m_Index;	int					m_SortColumn;};