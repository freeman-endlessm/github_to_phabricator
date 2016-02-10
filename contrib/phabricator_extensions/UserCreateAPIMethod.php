<?php

final class UserEnableConduitAPIMethod extends UserConduitAPIMethod {

  public function getAPIMethodName() {
    return 'user.create';
  }

  public function getMethodDescription() {
    return pht('Create users (admin only).');
  }

  protected function defineParamTypes() {
    return array(
      'username' => 'required string<username>',
      'realname' => 'required string<realname>',
      'email' => 'required string<email>',
    );
  }

  protected function defineReturnType() {
    return 'string<phid>';
  }

  protected function defineErrorTypes() {
    return array(
      'ERR-PERMISSIONS' => pht('Only admins can call this method.'),
      'ERR-INVALID-USERNAME' => pht('Invalid username'),
      'ERR-USER-EXISTS' => pht('User already exists'),
      'ERR-DUPLICATE-EMAIL' => pht('Duplicate email address'),
    );
  }

  protected function execute(ConduitAPIRequest $request) {
    $actor = $request->getUser();
    if (!$actor->getIsAdmin()) {
      throw new ConduitException('ERR-PERMISSIONS');
    }

    $username = $request->getValue('username');
    $realname = $request->getValue('realname');
    $create_email = $request->getValue('email');

    if (!PhabricatorUser::validateUsername($username)) {
      throw new ConduitException('ERR-INVALID-USERNAME');
    }

    if (!PhabricatorUserEmail::isAllowedAddress($create_email)) {
      throw new ConduitException('ERR-INVALID-EMAIL');
    }

    $users = id(new PhabricatorPeopleQuery())
      ->setViewer($request->getUser())
      ->withUsernames([$username])
      ->execute();

    if (count($users) != 0) {
      throw new ConduitException('ERR-USER-EXISTS');
    }

    # Verify Unique email
    #$duplicate = id(new PhabricatorUserEmail())->loadOneWhere(
    #  'address = %s',
    #  $create_email);
    #if ($duplicate) {
    #  throw new ConduitException('ERR-DUPLICATE-EMAIL');
    #}

    $user = new PhabricatorUser();
    $user->setUsername($username);
    $user->setRealName($realname);

    $user->openTransaction();

      $editor = new PhabricatorUserEditor();
      $editor->setActor($actor);

      $email = id(new PhabricatorUserEmail())
        ->setAddress($create_email)
        ->setIsVerified(1);

      $user->setIsApproved(1);
      $editor->createNewUser($user, $email);

    $user->saveTransaction();

    return $user->getPHID();

  }

}
