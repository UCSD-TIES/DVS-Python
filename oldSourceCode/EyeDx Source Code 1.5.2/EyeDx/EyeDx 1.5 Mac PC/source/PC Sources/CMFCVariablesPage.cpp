// main.cp#include <stdio.h>#include <windows.h>#include <wingdi.h>#include <winbase.h>#include <winuser.h>#include <process.h>#include "resource.h"#include "globals.h"#include "main.h"#include "DLLVersion.h"#if defined (WIN32)	#define IS_WIN32	TRUE#else	#define IS_WIN32	FALSE#endifIMPLEMENT_DYNCREATE(CMFCVariablesPage, CPropertyPage)BEGIN_MESSAGE_MAP( CMFCVariablesPage, CPropertyPage )ON_NOTIFY_EX(TTN_NEEDTEXT, 0, OnToolTipText)ON_BN_CLICKED(IDC_LAYOUTNEWBUTTON, OnNewPressed)ON_BN_CLICKED(IDC_LAYOUTEDITBUTTON, OnEditPressed)ON_BN_CLICKED(IDC_LAYOUTDELETEBUTTON, OnDeletePressed)ON_NOTIFY(NM_CLICK, IDC_LAYOUTVARIABLELIST, OnListClicked)ON_NOTIFY(NM_DBLCLK, IDC_LAYOUTVARIABLELIST, OnListDoubleClicked)ON_NOTIFY(LVN_COLUMNCLICK, IDC_LAYOUTVARIABLELIST, OnListColumnPressed)ON_NOTIFY(LVN_GETDISPINFO, IDC_LAYOUTVARIABLELIST, OnGetDispInfo)ON_WM_SIZE()END_MESSAGE_MAP()CEyeDxBooleanType CMFCVariablesPage::OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*){	TOOLTIPTEXT *pTTT = (TOOLTIPTEXT *) pNMHDR;	if (!(pTTT->uFlags & TTF_IDISHWND))	// the ID must be a handle to a window		return FALSE;			UINT uID = pNMHDR->idFrom;	uID = ::GetDlgCtrlID((HWND)uID);			CString strTipText;		// Attempt to load a ToolTip string that corresponds to the control's ID		if(!strTipText.LoadString(uID))		return FALSE;		// Stuff text into the ToolTip, 80 characters maximum		strncpy(pTTT->lpszText, strTipText, 80);	return TRUE;}const int kMaxVariableNameCharLength = 30;const int kMaxVariableNameDispLength = 180;const int kMaxVariableClassDispLength = 45;const int kMaxVariableTypeDispLength = 135;const int kMaxVariableDataTypeDispLength = 80;const int kMaxVariableRequiredDispLength = 250;CEyeDxBooleanType CMFCVariablesPage::OnInitDialog(){#ifdef DEBUG_PROPERTIESAfxMessageBox("C1", IDOK);#endif	CPropertyPage::OnInitDialog();	#ifdef DEBUG_PROPERTIESAfxMessageBox("C2", IDOK);#endif	m_VariableListBox = (CListCtrl *) GetDlgItem(IDC_LAYOUTVARIABLELIST);		// We have to check the version of the common controls DLL to see if we can use	// the full row select and grid lines features of the list control.	#ifdef DEBUG_PROPERTIESAfxMessageBox("C3", IDOK);#endif	CDLLVersion comCtrlsVersion("comctl32.dll");	#ifdef DEBUG_PROPERTIESAfxMessageBox("C4", IDOK);#endif	if ((comCtrlsVersion.GetMajorVersion() >= 4) && (comCtrlsVersion.GetMinorVersion() >= 70))	{#ifdef DEBUG_PROPERTIESAfxMessageBox("C5", IDOK);#endif		DWORD currentStyle = m_VariableListBox->SendMessage(LVM_GETEXTENDEDLISTVIEWSTYLE);		currentStyle |= (LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES);		m_VariableListBox->SendMessage(LVM_SETEXTENDEDLISTVIEWSTYLE, 0, (LPARAM)currentStyle);	}	#ifdef DEBUG_PROPERTIESAfxMessageBox("C6", IDOK);#endif	m_NewButton = (CButton *) GetDlgItem(IDC_LAYOUTNEWBUTTON);		m_EditButton = (CButton *) GetDlgItem(IDC_LAYOUTEDITBUTTON);		m_DeleteButton = (CButton *) GetDlgItem(IDC_LAYOUTDELETEBUTTON);		m_SingleDialogCheckbox = (CButton *) GetDlgItem(IDC_LAYOUTSEPARATEDIALOG);		if (m_PromptingStyle == kPromptOneAtATime)		m_SingleDialogCheckbox->SetCheck(BST_CHECKED);	else		m_SingleDialogCheckbox->SetCheck(BST_UNCHECKED);			m_EditButton->EnableWindow(FALSE);	m_EditButton->SetWindowText("&View...");	m_DeleteButton->EnableWindow(FALSE);#ifdef DEBUG_PROPERTIESAfxMessageBox("C7", IDOK);#endif	// Finally, add all of the controls to the resizer object		m_Resizer.Add(this, IDC_LAYOUTVARIABLELIST, RESIZE_LOCKALL);	m_Resizer.Add(this, IDC_LAYOUTNEWBUTTON, RESIZE_LOCKLEFT | RESIZE_LOCKBOTTOM);	m_Resizer.Add(this, IDC_LAYOUTEDITBUTTON, RESIZE_LOCKLEFT | RESIZE_LOCKBOTTOM);	m_Resizer.Add(this, IDC_LAYOUTDELETEBUTTON, RESIZE_LOCKLEFT | RESIZE_LOCKBOTTOM);	m_Resizer.Add(this, IDC_LAYOUTSEPARATEDIALOG, RESIZE_LOCKLEFT | RESIZE_LOCKBOTTOM);	#ifdef DEBUG_PROPERTIESAfxMessageBox("C8", IDOK);#endif	EnableToolTips(TRUE);		m_Modified = FALSE;	#ifdef DEBUG_PROPERTIESAfxMessageBox("C9", IDOK);#endif	// Create stupid bitmaps for list - I don't need them, but they have to exist! Grrr...		if (!m_imglLarge.Create(IDR_LARGEBLANK, 32, 1, RGB(255, 0, 255)))		return FALSE;		#ifdef DEBUG_PROPERTIESAfxMessageBox("C10", IDOK);#endif	if (!m_imglSmall.Create(IDR_SMALLBLANK, 16, 1, RGB(255, 0, 255)))		return FALSE;#ifdef DEBUG_PROPERTIESAfxMessageBox("C11", IDOK);#endif	CImageList *OldLargeList = m_VariableListBox->SetImageList(&m_imglLarge, LVSIL_NORMAL);	CImageList *OldSmallList = m_VariableListBox->SetImageList(&m_imglSmall, LVSIL_SMALL);#ifdef DEBUG_PROPERTIESAfxMessageBox("C12", IDOK);#endif	if (m_VariableListBox->InsertColumn(0, "Name", LVCFMT_LEFT, kMaxVariableNameDispLength) == -1)		return FALSE;#ifdef DEBUG_PROPERTIESAfxMessageBox("C13", IDOK);#endif	if (m_VariableListBox->InsertColumn(1, "Class", LVCFMT_LEFT, kMaxVariableClassDispLength) == -1)		return FALSE;#ifdef DEBUG_PROPERTIESAfxMessageBox("C14", IDOK);#endif	if (m_VariableListBox->InsertColumn(2, "Type", LVCFMT_LEFT, kMaxVariableTypeDispLength) == -1)		return FALSE;#ifdef DEBUG_PROPERTIESAfxMessageBox("C15", IDOK);#endif	if (m_VariableListBox->InsertColumn(3, "Data Type", LVCFMT_LEFT, kMaxVariableDataTypeDispLength) == -1)		return FALSE;#ifdef DEBUG_PROPERTIESAfxMessageBox("C16", IDOK);#endif	if (m_VariableListBox->InsertColumn(4, "Other Attributes", LVCFMT_LEFT, kMaxVariableRequiredDispLength) == -1)		return FALSE;	#ifdef DEBUG_PROPERTIESAfxMessageBox("C17", IDOK);#endif	int theImageCount = m_imglLarge.GetImageCount();	theImageCount = m_imglSmall.GetImageCount();		m_SortColumn = kSortColumnByName;		m_Index = -1;	#ifdef DEBUG_PROPERTIESAfxMessageBox("C18", IDOK);#endif	UpdateVariableList(NULL);		#ifdef DEBUG_PROPERTIESAfxMessageBox("C19", IDOK);#endif	return TRUE;}void CMFCVariablesPage::OnSize(UINT nType, int cx, int cy) {	CPropertyPage::OnSize(nType, cx, cy);	// Resize!	m_Resizer.Resize(this);	}void CMFCVariablesPage::OnOK(){	if (m_SingleDialogCheckbox->GetCheck() == BST_CHECKED)		m_PromptingStyle = kPromptOneAtATime;	else		m_PromptingStyle = kPromptAllInOne;}void CMFCVariablesPage::UpdateButtons(CEyeDxVariable *theVariable){	if (theVariable == NULL)	{		m_EditButton->EnableWindow(FALSE);		m_EditButton->SetWindowText("&Edit...");		m_DeleteButton->EnableWindow(FALSE);	}	else if (theVariable->GetVariableClass() == CEyeDxVariable::kUser)	{		m_EditButton->EnableWindow(TRUE);		m_EditButton->SetWindowText("&Edit...");		m_DeleteButton->EnableWindow(TRUE);	}	else	{		m_EditButton->EnableWindow(TRUE);		m_EditButton->SetWindowText("&View...");		m_DeleteButton->EnableWindow(FALSE);	}		}void CMFCVariablesPage::OnNewPressed(){	// Create a new variable for editing		CEyeDxVariable *theVariable = new CEyeDxVariable(CEyeDxVariable::kUser);		if (HandleEditVariable(m_VariableList, theVariable, TRUE, m_showHidden) == true)	{		// Add the new variable to both the local list (the one shown in the menus and scrolling list)		// and the full global list				m_VariableList->AddVariable(theVariable);				UpdateVariableList(theVariable);			UpdateButtons(theVariable);				// The HandleEditVariable routine handles the CancelToClose call if necessary		// DON'T DO IT HERE!	}	else		delete theVariable;}void CMFCVariablesPage::EditItem(int theItem){	CString theName = m_VariableListBox->GetItemText(theItem, 0);		// Save the variable that is selected		CEyeDxVariable *theVariable = m_VariableList->GetVariableByName(theName);		UpdateButtons(theVariable);	if (HandleEditVariable(m_VariableList, theVariable, FALSE, m_showHidden) == true)		UpdateVariableList(theVariable);	}void CMFCVariablesPage::OnListDoubleClicked(NMHDR *pnmh, LRESULT *pResult){	DWORD dwPos = ::GetMessagePos();	CPoint point ((int) LOWORD(dwPos), (int) HIWORD(dwPos));	m_VariableListBox->ScreenToClient(&point);	if ((m_Index = m_VariableListBox->HitTest(point)) != -1)		EditItem(m_Index);}	void CMFCVariablesPage::OnEditPressed(){	// Look up the variable that is currently selected and confirm that they want to delete it	// We always have to do a lookup because if the user sorts the list, the index of the selected	// variable changes.			m_Index = m_VariableListBox->GetNextItem(-1, LVNI_SELECTED);	if (m_Index >= 0)		EditItem(m_Index);}void CMFCVariablesPage::OnDeletePressed(){	// Look up the variable that is currently selected and confirm that they want to delete it			m_Index = m_VariableListBox->GetNextItem(-1, LVNI_SELECTED);	if (m_Index >= 0)	{								CString theName = m_VariableListBox->GetItemText(m_Index, 0);				CEyeDxVariable *theVariable = m_VariableList->GetVariableByName(theName);							CString theMessage;		theMessage.Format("Are you sure you want to delete the variable %s (no undo!)?", theName);				if (MessageBox(theMessage, AfxGetAppName(), MB_YESNO) == IDYES)		{			m_VariableList->DeleteVariableByName(theName);			UpdateVariableList(NULL);				CancelToClose();			UpdateButtons(NULL);		}	}			}void CMFCVariablesPage::OnListClicked(NMHDR *pnmh, LRESULT *pResult){	DWORD dwPos = ::GetMessagePos();	CPoint point ((int) LOWORD(dwPos), (int) HIWORD(dwPos));	m_VariableListBox->ScreenToClient(&point);		m_Index = m_VariableListBox->HitTest(point);		if (m_Index >= 0)	{								CString theName = m_VariableListBox->GetItemText(m_Index, 0);				CEyeDxVariable *theVariable = m_VariableList->GetVariableByName(theName);		UpdateButtons(theVariable);		}}void CMFCVariablesPage::OnListColumnPressed(NMHDR *pnmh, LRESULT *pResult){	NM_LISTVIEW *pnmlv = (NM_LISTVIEW *) pnmh;		// We don't sort on the 4th column ("Other Attributes")	if (pnmlv->iSubItem != kSortColumnByOtherAttributes)	{		m_SortColumn = pnmlv->iSubItem;		m_VariableListBox->SortItems(CEyeDxVariable::CompareFunc, pnmlv->iSubItem);	}		// Look up the selected item and try to make it visible	m_Index = m_VariableListBox->GetNextItem(-1, LVNI_SELECTED);	if (m_Index >= 0)		m_VariableListBox->EnsureVisible(m_Index, FALSE);}void CMFCVariablesPage::OnGetDispInfo(NMHDR *pnmh, LRESULT *pResult){	CString theString;		LV_DISPINFO * plvdi = (LV_DISPINFO *) pnmh;		if (plvdi->item.mask & LVIF_TEXT)	{		CEyeDxVariable *theVariable = (CEyeDxVariable *)plvdi->item.lParam;				switch (plvdi->item.iSubItem)		{		case 0:	// Name					CString *theName = theVariable->GetName();			theString = theName->Left(kMaxVariableNameCharLength);						break;				case 1:	// Class								// If the variable is hidden, display that instead of the class						if (theVariable->GetVariableIsHidden())				theString = "Hidden";			else			{				switch (theVariable->GetVariableClass())				{				case CEyeDxVariable::kUser:					theString = "User";					break;									case CEyeDxVariable::kEyeDx:					theString = "EyeDx";					break;				}				}			break;				case 2:	// Type					switch (theVariable->GetVariableType())			{			case CEyeDxVariable::kFixed:				theString = "Fixed";				break;							case CEyeDxVariable::kPrompted:				switch (theVariable->GetWhenToPrompt())				{				case CEyeDxVariable::kPromptNone:					theString = "No Prompt";					break;									case CEyeDxVariable::kPromptOnStart:					theString = "Prompt: On Startup";					break;				case CEyeDxVariable::kPromptForSubject:					theString = "Prompt: Each Subject";					break;								case CEyeDxVariable::kPromptForSession:					theString = "Prompt: Each Session";					break;								case CEyeDxVariable::kPromptForEndOfSession:					theString = "Prompt: End of Session";					break;				case CEyeDxVariable::kPromptDisabled:					theString = "Prompt: Disabled";					break;				}										break;							case CEyeDxVariable::kCalculated:				theString = "Calculated";				break;			}							break;					case 3:	// Data Type					switch (theVariable->GetDataType())			{			case CEyeDxVariable::kTypeNone:			case CEyeDxVariable::kGeneralString:				theString = "String";				break;							case CEyeDxVariable::kDate:				theString = "Date";				break;			case CEyeDxVariable::kPastDate:				theString = "Past Date";				break;						case CEyeDxVariable::kTime:				theString = "Time";				break;						case CEyeDxVariable::kIntegerNumber:				theString = "Number";				break;			case CEyeDxVariable::kCheckBox:				theString = "Check Box";				break;			case CEyeDxVariable::kMenu:				theString = "Menu";				break;			}					break;					case 4:	// Other attributes					// If the variable is prompted, then indicate whether it is required or not			// If a fixed value, show the value in quotes. Otherwise, just display a blank.						CString *theValueStr;			theString = "";						switch (theVariable->GetVariableType())			{			case CEyeDxVariable::kPrompted:				// We only show optional/required if the prompted variable isn't disabled (it would				// be confusing to say it's required if it's disabled!).								if (theVariable->GetWhenToPrompt() != CEyeDxVariable::kPromptDisabled)				{					if (theVariable->GetValueMustBeEntered())						theString = "(Required Entry)";					else						theString = "(Optional Entry)";				}				break;			case CEyeDxVariable::kFixed:				theString = "\"";				theValueStr = theVariable->GetValue();				theString += *theValueStr;				theString += "\"";				break;			}			break;		}		::lstrcpy(plvdi->item.pszText, (LPCTSTR) theString);	}}			void CMFCVariablesPage::UpdateVariableList(CEyeDxVariable *reselectVariable){	LV_ITEM lvi;				// We first delete all of the items from the variable scrolling list		m_VariableListBox->DeleteAllItems();			// Now we add all of the variables to the list box		m_VariableListBox->SendMessage(WM_SETREDRAW, FALSE, 0);		int theItemCount = m_VariableList->GetCount();		for (long theItem = 0; theItem < theItemCount; theItem++)	{		CEyeDxVariable *theVariable = m_VariableList->GetVariableByIndex(theItem);				if (m_showHidden || !theVariable->GetVariableIsHidden())		{			CEyeDxLongStringType *theName = theVariable->GetName();						lvi.mask = LVIF_TEXT | LVIF_PARAM | LVIF_IMAGE;			lvi.iItem = theItem;			lvi.iSubItem = 0;			lvi.iImage = 0;			lvi.pszText = *theName;			lvi.lParam = (LPARAM) theVariable;			lvi.state = 0;			lvi.stateMask = 0;			lvi.iIndent = 0;						// Reselect the variable if it was previously selected						if (reselectVariable == theVariable)			{				lvi.mask |= LVIF_STATE;				lvi.state = LVIS_SELECTED;				lvi.stateMask = LVIS_SELECTED;			}						if (m_VariableListBox->InsertItem(&lvi) == -1)				return;					}	}		m_VariableListBox->SendMessage(WM_SETREDRAW, TRUE, 0);		// Finally, we resort the list if it wasn't previously sort by name		if (m_SortColumn != kSortColumnByName)		m_VariableListBox->SortItems(CEyeDxVariable::CompareFunc, m_SortColumn);	// Try to scroll the selected item into view. Since the items are rearranged in	// alphabetical order when we insert them, and when they are optionally sorted	// by another column, we have to look up the item's index again.		if (reselectVariable)	{		m_Index = m_VariableListBox->GetNextItem(-1, LVNI_SELECTED);		if (m_Index >= 0)			m_VariableListBox->EnsureVisible(m_Index, FALSE);	}		}	BOOL CMFCVariablesPage::HandleEditVariable(CEyeDxVariableList *theVariableList, CEyeDxVariable *theVariable, BOOL newVariable, BOOL showHidden){	CMFCEditVariableDlg dlg(this, theVariableList, theVariable, newVariable, showHidden);	if (dlg.DoModal() == IDOK)	{		// If the variable is an EyeDx variable, they couldn't change it, therefore,		// don't prevent cancelling				if (theVariable->GetVariableClass() != CEyeDxVariable::kEyeDx)			CancelToClose();					return TRUE;	}	else		return FALSE;}void CMFCVariablesPage::DoDataExchange(CDataExchange *pDX){	CPropertyPage::DoDataExchange(pDX);}