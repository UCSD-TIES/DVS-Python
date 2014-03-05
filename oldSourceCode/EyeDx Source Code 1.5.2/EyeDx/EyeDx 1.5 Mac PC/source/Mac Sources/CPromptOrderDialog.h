// =================================================================================//	CPromptOrderDialog.h				�1995 Metrowerks Inc. All rights reserved.// =================================================================================//	CPromptOrderDialog.cp	#pragma once#include <LGADialog.h>#include <LEditField.h>#include <LStdControl.h>#include <LTextTableView.h>#include <LCellSizeToFit.h>#include <LTableSingleRowSelector.h>#include <LTableMultiGeometry.h>#include <LTableArrayStorage.h>#include "CEyeDxVariables.h"class CPromptOrderDialog : public LGADialog {public:	enum { class_ID = 'PorD' };								CPromptOrderDialog( LStream *inStream );								~CPromptOrderDialog();	virtual void				ListenToMessage(MessageT	inMessage, void		*ioParam);	virtual void				SetupDialog(CEyeDxVariableList *theVariableList, CEyeDxVariable::PromptType thePromptType);	protected:	virtual void				FinishCreateSelf();		void						UpdateVariableList();		CEyeDxVariableList			*mVariableList;	CEyeDxVariableList			*mSortedVariableList;	LTextTableView				*mVariableTable;	CEyeDxButtonType			*mMoveUpButton;	CEyeDxButtonType			*mMoveDownButton;	CEyeDxRadioButtonType		*mAllAtOnceButton;	CEyeDxRadioButtonType		*mSeparateDialogsButton;	CEyeDxButtonType			*mCancelButton;	CEyeDxButtonType			*mSaveButton;	LTableSingleRowSelector 	*mTableSelector;	LTableMultiGeometry 		*mTableGeometry;	LTableArrayStorage 			*mTableStorage;};